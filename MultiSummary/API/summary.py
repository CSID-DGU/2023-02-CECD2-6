from typing import Union,List
from fastapi import FastAPI
from pydantic import BaseModel
from getNewsData import get_news_data
from summaryArgs import parse_args
import kss
import sys

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
    for i, new in enumerate(news):
        print(f'{i}번째:')
        print(new)

    #DB에서 가져온 값으로 클러스터링
    articles_by_topic=Custer(news).hierachyClustering()
    
    # 요약모델 사용
    summarys=[]
    for i, articles in enumerate(articles_by_topic.values()):
        data=[]
        print(f'{i}번째')
        for article in articles:
            data.append(kss.split_sentences(article))

        summary=summarize(data,args, device_id, cp, step)
        summarys.append(summary)
        data=[]
    print(summarys)

    return {"summary": f"{summarys}"}