from prepro.data_builder import BertData
from models.model_builder import ExtSummarizer
from prepro.preprocessor_kr import korean_sent_spliter, preprocess_kr

import torch
import numpy as np

from models import data_loader
from models.trainer_ext import build_trainer

from others.logging import logger

from tqdm import tqdm

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
    #print(summarizedText)

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
