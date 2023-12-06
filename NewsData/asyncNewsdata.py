#-*- coding: utf-8 -*-
from RSS.RSS import RSS
from textrank.TextRank import TextRank
import json
import psycopg2
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
import aiohttp
import asyncio

env_path=os.environ.get('GDSPATH', os.environ.get('HOME')+'\\2023-02-CECD2-6')+'\\NewsData\\DBConfig.env'
env_path=env_path.replace('\\','/')
load_dotenv(env_path)

DB_CONNECT_HOST=os.environ.get("DB_HOST")
DB_CONNECT_DBNAME=os.environ.get("DB_NAME")
DB_CONNECT_USER=os.environ.get("DB_USER")
DB_CONNECT_PWD=os.environ.get("DB_PWD")
DB_CONNECT_PORT=os.environ.get("DB_PORT")

# 데이터베이스 연결
conn = psycopg2.connect(host=DB_CONNECT_HOST, dbname=DB_CONNECT_DBNAME, user=DB_CONNECT_USER, password=DB_CONNECT_PWD, port=int(DB_CONNECT_PORT))
cur = conn.cursor()

async def sendAsyncRequest(url):
    async with aiohttp.ClientSession() as session:
        await session.get(url)

def newsData():
    # RSS를 통한 뉴스 데이터 수집
    result = RSS()

    # dictionary 형태의 결과물에서 뉴스 기사별로 조회
    for company in result:
        companyName = result[company]["companyName"]
        
        for topic in result[company]["articles"]:
            for news in result[company]["articles"][topic]:
                title = str(news["title"])
                link = news["link"]
                context = news["context"]
                date = news["date"]
                
                # TextRank를 통한 키워드 추출 및 데이터베이스 저장
                try:
                    keywords = TextRank(context)
                    combinedContext = '.?.'.join(context)
                    # cur.execute("insert into news(companyname, topic, title, link, context, keywords) values(%s, %s, %s, %s, %s, %s);", (companyName, topic, title, link, context, keywords))
                    cur.execute("insert into news(company_name, topic, title, link, context, post_time) values(%s, %s, %s, %s, %s, %s);", (companyName, topic, title, link, combinedContext, date))
                    conn.commit()
                    
                    cur.execute("select id from news order by id desc limit 1;")
                    row = cur.fetchone()
                    
                    id = row[0]
                    
                    for keyword in keywords:
                        cur.execute("insert into newskeyword(news_id, keyword) values(%s, %s);", (id, keyword))
                        conn.commit()
                except UnicodeDecodeError: # 특수 문자에 대한 예외 처리
                    continue
                except ValueError: # TextRank로 처리하기 힘든 적은 문자수의 기사의 경우 생략
                    continue                    
                    
async def main():
    try:
        print(f"Start At [{datetime.now().strftime('%H:%M:%S')}]")
        newsData()
        print('newsData - executed successfully')
    except Exception as e:
        print('newsData - failed')

    task = asyncio.create_task(sendAsyncRequest("http://GDSLoadBalancer-590554331.ap-northeast-2.elb.amazonaws.com/summary/rsscomplete"))
    await asyncio.sleep(5)

asyncio.run(main())