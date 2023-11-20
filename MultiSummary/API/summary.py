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

    #DB에서 가져온 값으로 클러스터링
    start_time = time.time()
    #articles_by_topic=Custer(news).hierachyClustering()
    articles_by_topic=Custer(news).silhouette_analysis(int(len(news)*0.8))
    
    # 요약모델 사용
    summarys=[]
    for articles in tqdm(articles_by_topic.values(),desc="요약 중"):
        data=[]
        for article in articles:
            data.append(kss.split_sentences(article))
       
        summary=summarize(data,args, device_id, cp, step)
        summarys.append(summary)
        
        #군집별 Rouge Score 계산(필요시 주석 제거)
        '''    
        scorer = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rouge3', 'rouge4', 'rougeL'], use_stemmer=True)
        rouge_scores = scorer.score(' '.join(articles), ' '.join(summary))
        print(rouge_scores)
        '''

        data=[]
    end_time = time.time()

    print(summarys)
    execution_time = end_time - start_time
    print(f"코드 실행 시간: {execution_time} 초")

    return {"summary": f"{summarys}"}