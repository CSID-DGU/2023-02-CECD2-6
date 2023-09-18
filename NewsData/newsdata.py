from RSS.RSS import RSS
from textrank.TextRank import TextRank
import json

def newsData():
    # result = RSS()
    with open('output.json', 'r', encoding='utf-8') as f:
        result = json.load(f)
    
    for company in result:
        for _ in result[company]:
            companyName = result[company]["companyName"]
            
            for topic in result[company]["articles"]:
                for news in result[company]["articles"][topic]:
                    title = news["title"]
                    link = news["link"]
                    context = news["context"]
                    if len(context) <= 1: continue
                    # print(context)
                    
                    try:
                        keywords = TextRank(context)
                        print(companyName, topic, title, link, keywords)
                        break
                    except UnicodeDecodeError: # 특수 문자에 대한 예외 처리
                        continue
                        
                    
                    
    
newsData()