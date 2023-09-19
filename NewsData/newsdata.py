from RSS.RSS import RSS
from textrank.TextRank import TextRank
import json
import psycopg2

# 데이터베이스 연결
conn = psycopg2.connect(host="127.0.0.1", dbname="root", user="root", password="1234", port=5432)
cur = conn.cursor()

def newsData():
    # RSS를 통한 뉴스 데이터 수집
    result = RSS()


    # dictionary 형태의 결과물에서 뉴스 기사별로 조회
    for company in result:
        for _ in result[company]:
            companyName = result[company]["companyName"]
            
            for topic in result[company]["articles"]:
                for news in result[company]["articles"][topic]:
                    title = str(news["title"])
                    link = news["link"]
                    context = news["context"]
                    
                    # TextRank를 통한 키워드 추출 및 데이터베이스 저장
                    try:
                        keywords = TextRank(context)
                        cur.execute("insert into news(companyname, topic, title, link, context, keywords) values(%s, %s, %s, %s, %s, %s);", (companyName, topic, title, link, context, keywords))
                        conn.commit()
                    except UnicodeDecodeError: # 특수 문자에 대한 예외 처리
                        continue
                    except ValueError: # TextRank로 처리하기 힘든 적은 문자수의 기사의 경우 생략
                        continue
                    
                    
    
newsData()