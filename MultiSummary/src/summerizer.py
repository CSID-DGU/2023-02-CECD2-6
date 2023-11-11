from prepro.data_builder import BertData
from models.model_builder import ExtSummarizer
from prepro.preprocessor_kr import korean_sent_spliter, preprocess_kr

import torch
import numpy as np

from models import data_loader
from models.trainer_ext import build_trainer

from others.logging import logger

from tqdm import tqdm

import networkx as nx
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def summarize(rawData,args,device_id, cp, step):
    #data Json 형태로 바꾸어주기 
    json_list = []
    for article in rawData:
        src_sents = (
            article
            if isinstance(article, list)
            else korean_sent_spliter(article)
        )
        original_sents_list = [preprocess_kr(sent).split() for sent in src_sents]

        json_list.append({"src": original_sents_list})
    #print(json_list)

    bertData=json_to_bert(json_list,args)
    
    #summary_list=[]
    #for i in range(len(rawData)):
    #    summary_list.append(predict_summary(bertData[i],rawData[i],args,cp))
    #return summary_list

    device = "cpu" if args.visible_gpus == '-1' else "cuda"

    checkpoint = torch.load(cp)  # V3 - max_pos 1024
    model = ExtSummarizer(args, device, checkpoint)
    model.eval()

    opt = vars(checkpoint['opt'])
    model_flags = ['hidden_size', 'ff_size', 'heads', 'inter_layers', 'encoder', 'ff_actv', 'use_interval', 'rnn_size']
    for k in opt.keys():
        if (k in model_flags):
            setattr(args, k, opt[k])

    test_iter = data_loader.Dataloader(args, load_Bert(bertData),
                                       args.test_batch_size, device,
                                       shuffle=False, is_test=True)

    trainer = build_trainer(args, device_id, model,None)
    summarizedText=trainer.test(test_iter, step)
    print(f'단일 요약문:{summarizedText}\n')

    conbinedText=textRank(summarizedText)
    print(f'중요도 순으로 결합한 요약문:{conbinedText}\n')
    
    result = remove_duplicateSentence(conbinedText)
    print(f'최종 요약문: {result}\n')
    '''
    #Bert를 이용하는 방법
    print(len(conbinedText))
    json_list = []
    for article in [conbinedText]:
        src_sents = (
            article
            if isinstance(article, list)
            else korean_sent_spliter(article)
        )
        original_sents_list = [preprocess_kr(sent).split() for sent in src_sents]

        json_list.append({"src": original_sents_list})
    #print(json_list)

    bertData=json_to_bert(json_list,args)
    
    #summary_list=[]
    #for i in range(len(rawData)):
    #    summary_list.append(predict_summary(bertData[i],rawData[i],args,cp))
    #return summary_list
    print(bertData)
    device = "cpu" if args.visible_gpus == '-1' else "cuda"

    checkpoint = torch.load(cp)  # V3 - max_pos 1024
    model = ExtSummarizer(args, device, checkpoint)
    model.eval()

    opt = vars(checkpoint['opt'])
    model_flags = ['hidden_size', 'ff_size', 'heads', 'inter_layers', 'encoder', 'ff_actv', 'use_interval', 'rnn_size']
    for k in opt.keys():
        if (k in model_flags):
            setattr(args, k, opt[k])

    test_iter = data_loader.Dataloader(args, load_Bert(bertData),
                                       args.test_batch_size, device,
                                       shuffle=False, is_test=True)

    trainer = build_trainer(args, device_id, model,None)
    conbinedText=trainer.combine_summarizer(test_iter, step)
    #print(conbinedText)



    #'''

#json bert 변환
def json_to_bert(dataJson,args):
    bert = BertData(args)
    jobs = dataJson

    datasets = []
    for d in tqdm(jobs, desc="bert 변환 중"):
        source = d["src"]
        source = [" ".join(s).lower().split() for s in source]
        
        b_data = bert.preprocess(
            source,
            use_bert_basic_tokenizer=False,
            is_test=True,
        )

        if b_data is None:
            continue
        (
            src_subtoken_idxs,
            segments_ids,
            cls_ids,
            src_txt,
        ) = b_data
        b_data_dict = {
            "src": src_subtoken_idxs,
            "segs": segments_ids,
            "clss": cls_ids,
            "src_txt": src_txt,
        }
        datasets.append(b_data_dict)
    #print(datasets)
    return datasets

#BertData load
def load_Bert(Bert):
    def _lazy_dataset_loader(Bert):

        logger.info(
            "number of examples: %d"
            % (len(Bert))
        )
        return Bert

    yield _lazy_dataset_loader(Bert)

#예측부
def predict_summary(bertData,rawData,args,cp):
    input_data = [bertData]
    device = torch.device("cpu")


    pre_src = [x['src'] for x in input_data]
    pre_segs = [x['segs'] for x in input_data]
    pre_clss = [x['clss'] for x in input_data]

    src = torch.tensor(_pad(pre_src, 0), device=device)
    segs = torch.tensor(_pad(pre_segs, 0), device=device)
    mask_src = ~(src == 0)

    clss = torch.tensor(_pad(pre_clss, -1), device=device)
    mask_cls = ~(clss == -1)
    clss[clss == -1] = 0

    clss.to(device).long()
    mask_cls.to(device).long()
    segs.to(device).long()
    mask_src.to(device).long()

    checkpoint = torch.load(cp)  # V3 - max_pos 1024
    model = ExtSummarizer(args, device, checkpoint)
    model.eval()

    with torch.no_grad():
        sent_scores, mask = model(src, segs, clss, mask_src, mask_cls)
        sent_scores = sent_scores + mask.float()
        sent_scores = sent_scores.cpu().data.numpy()
        print(sent_scores)
        selected_ids = np.argsort(-sent_scores, 1)
        print(selected_ids)


    #print(selected_ids)

    #result를 조정하여 요약 정도를 나타낼 수 있음.  
    result =[rawData[i] for i in selected_ids[0][:len(rawData)//3]]
    print(result)
    return result

def _pad(data, pad_id, width=-1):
    if (width == -1):
        width = max(len(d) for d in data)
    rtn_data = [d + [pad_id] * (width - len(d)) for d in data]
    return rtn_data

#textRank를 이용한 요약문 결합
def textRank(summarizedText):
    conbinedText=[]
    for  ariticle in summarizedText:
        for text in  ariticle:
            conbinedText.append(text)

    # TF-IDF 벡터화
    tfidf = TfidfVectorizer()
    tfidf_matrix = tfidf.fit_transform(conbinedText)

    # 문장 간 유사도 계산 (cosine similarity)
    similarity_matrix = (tfidf_matrix * tfidf_matrix.T).A
    graph = nx.from_numpy_array(similarity_matrix)

    # TextRank 스코어 계산
    scores = nx.pagerank(graph)
    print(scores)

    # 문장을 TextRank 스코어에 따라 정렬
    ranked_sentences = sorted(((scores[i], sentence) for i, sentence in enumerate(conbinedText)), reverse=True)

    conbinedText=[]
    for i, (score, sentence) in enumerate(ranked_sentences):
        print(f"Sentence {i + 1}: Score: {score:.4f}, Sentence: {sentence}")
        conbinedText.append(sentence)

    #print(conbinedText)
    return conbinedText

def mmr_score(query, sentence, lambda_param=0.7):
    # TF-IDF 벡터화
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([query, sentence])

    # 코사인 유사도 계산
    similarity = cosine_similarity(tfidf_matrix)[0][1]

    # 문장 길이 비율 계산
    length_ratio = len(sentence.split()) / len(query.split())
    query_length = len(query.split())
    
    # MMR 스코어 계산 (수정)
    mmr_score = lambda_param * similarity - (1 - lambda_param) * (length_ratio / query_length)

    return mmr_score

def remove_duplicateSentence(sentences):
    result=[sentences[0]]
    regard=[]
    # MMR 스코어를 기준으로 중복을 걸러냄
    for i,sentence in enumerate(sentences[1:], start=1):
        query_sentence=sentence
        mmr_scores = [mmr_score(query_sentence, s) for s in sentences]
        
        # MMR 스코어가 가장 높은 문장 선택
        max_score_index =max(((idx, val) for idx, val in enumerate(mmr_scores) if idx != i), key=lambda x: x[1])[0]
        max_score_sentence = list(sentences)[max_score_index]
        #print(f'제시문:{sentence}')
        #print(f'해당 문장과 가장 비슷하다고 여겨지는 문장: {max_score_sentence}={max_score_index}번째 줄')
        #print(mmr_scores)

        #비슷하다고 여겨지는 문장이 결과문에 존재하지 않으면 현재 쿼리가 되는 문장을 넣어줌
        if max_score_sentence not in result:
            result.append(query_sentence)

        #주제와 벗어난 문장 처리하기
        total_sentences= len(sentences) #전체 문장수 
        unrelated_sentence = int(total_sentences * 0.4)
        count_below_minus_5 = sum(1 for value in mmr_scores if value <= -0.5) #이 부분 숫자 전체 뮨장 비율로 나타내주

        #관련도가 없다고 여긴 문장이 전체의 40%면 제거할 대상으로 들어감
        if count_below_minus_5 >= unrelated_sentence:
            regard.append(query_sentence)



    #관련도가 없는 문장들은 결과문에서 제거해줌
    #print(regard)
    for element in regard:
        if element in result:
            result.remove(element)

    return result
