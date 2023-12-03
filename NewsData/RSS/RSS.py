import RSS.newsGenerator as newsGenerator
import json
import RSS.utils as utils
from datetime import datetime, timedelta

# 테스트용 import
import time

'''
    필요시 데이터 후처리 가능
    {
        "언론사 영어이름": {
            "companyName":"언론사 한글이름",
            "articles": {
                "topic1": [
                    {
                        "title":title,
                        "link":link,
                        "context":[sentence1, sentence2, ...]
                    }
                ],
                "topic2": [
                    {
                        "title":title,
                        "link":link,
                        "context":[sentence1, sentence2, ...]
                    }
                ],
            }
        }
    }
'''

# 최종 결과 후처리 함수, input 형태는 위의 주석 참고
def PostProcessing(inputDict):
    for companyNameENG in inputDict.keys():
        companyName=inputDict[companyNameENG]['companyName']
        articleDict=inputDict[companyNameENG]['articles']

        for topic in articleDict.keys():
            articleList=articleDict[topic]

            for idx in range(len(articleList)):
                article=articleList[idx]
                title=article['title']
                link=article['link']
                context=article['context']

                for contextIdx in range(len(context)):
                    sentence=context[contextIdx]
                    # 1. 양옆 공백제거
                    sentence=sentence.strip()

                    # 2. 문장 html 태그 제거
                    sentence=utils.removeHtmlTags(sentence)

                    # 3. 문장 html 엔티티 변환
                    sentence=utils.convertHtmlEntities(sentence)

                    # 4. escape 요소 제거
                    sentence=sentence.encode().decode('unicode_escape')
                    
                    context[contextIdx] = sentence

# 뉴스기사 생략 조건 판정 함수
'''
    입력: {"title"=title,"link"=link,"date"=date} Dictonary, 언론사 이름, 주제 이름
'''
def skipCondition(news,cName,cTopic):
    lastPostDict = utils.LoadJsonFile(utils.getHomePath('NewsData/RSS/lastPost.json'))
    try:
        # 포스트 시간은 지금부터 하루전
        if(utils.CompareTimeStamp((datetime.now()-timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S"),news['date'])>=0):
            return True

        # lastPost.json이 없으면 스킵을 하지 않는다.
        if(lastPostDict is None):
            return False

        # 마지막 포스팅 시간보다 빠르게 나온 기사는 스킵
        if(utils.CompareTimeStamp(lastPostDict[cName][cTopic],news['date'])>=0):
            return True

        # title이 '[사진]'으로 시작하는 기사는 스킵
        if(news['title'].startswith('[사진]')):
            return True

    except Exception:
        return False
    return False

def RSS():
    data_dict={}
    data_dict = newsGenerator.GetNewsArticle_AllMediaCompany(False,skipCondition,PostProcessing)
    return data_dict