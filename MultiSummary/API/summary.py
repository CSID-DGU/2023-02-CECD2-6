from typing import Union,List
from fastapi import FastAPI
from pydantic import BaseModel
from tqdm import tqdm
from getNewsData import get_news_data
from summaryArgs import parse_args
from rouge_score import rouge_scorer
import kss
import sys
import time

sys.path.append("../src")
from summerizer import summarize
from multiSummarizer.clustering import Custer
from multiSummarizer.suffix_unification  import convert_to_formal_korean

app = FastAPI()

class NumberList(BaseModel):
    numbers: List[int]

@app.post("/summary/")
async def createSummary(number_list: NumberList):
    #인자 
    args, cp, step = parse_args()
    device = "cpu" if args.visible_gpus == "-1" else "cuda"
    device_id = 0 if device == "cuda" else -1

    #뉴스데이터 가져오기 
    news=get_news_data(number_list.numbers)

    if(int(len(news))!=0):
        #DB에서 가져온 값으로 클러스터링
        start_time = time.time()
        #articles_by_topic=Custer(news).hierachyClustering()
        #articles_by_topic=Custer(news).silhouette_analysis_with_score(int(len(news)*0.8))

        articles_by_topic=Custer(news).silhouette_analysis(int(len(news)*0.8))
        

        # 요약모델 사용
        summarys=[]
        rouge_scores_list = []  # 군집별 Rouge 스코어 저장 리스트
        for articles in tqdm(articles_by_topic.values(),desc="요약 중"):
            try:
                data=[]
                for article in articles:
                    data.append(kss.split_sentences(article))
            
                summary=summarize(data,args, device_id, cp, step)
                converted_summary = convert_to_formal_korean(' '.join(summary))
                summarys.append(converted_summary)
                
                #군집별 Rouge Score 계산(필요시 주석 제거)
                    
                scorer = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rouge3', 'rouge4', 'rougeL'], use_stemmer=True)
                rouge_scores = scorer.score(' '.join(articles), ' '.join(summary))
                print(rouge_scores)
                
                rouge_scores_list.append(rouge_scores)
                data=[]
            except:
                print("pass")
        end_time = time.time()
        
        # 군집별로 계산한 Rouge 스코어 평균 계산
        average_rouge_scores = {metric: sum(score[metric].fmeasure for score in rouge_scores_list) / len(rouge_scores_list) for metric in ['rouge1', 'rouge2', 'rouge3', 'rouge4', 'rougeL']}
        print("Average Rouge Scores:")
        for metric, score in average_rouge_scores.items():
            print(f'{metric}: {score}')

        print(summarys)
        execution_time = end_time - start_time
        print(f"코드 실행 시간: {execution_time} 초")

        return {"summary": f"{summarys}"}
    else:
        return {"summary": f""}