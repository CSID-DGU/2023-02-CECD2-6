from RSS.RSS import RSS
import json

def newsData():
    # RSS를 통한 뉴스 데이터 수집
    result = RSS()

    with open('output.json', 'w',encoding='utf-8') as f:
        json.dump(result, f,ensure_ascii=False)
              
newsData()