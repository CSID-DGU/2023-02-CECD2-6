import RSS.newsGenerator as newsGenerator
import json
import RSS.utils as utils

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
                    
                    context[contextIdx] = sentence

# 생략 조건 판정 함수
'''
    입력: {"title"=title,"link"=link} Dictonary
'''
def skipCondition(news):
    return False

def RSS():
    data_dict={}
    data_dict = newsGenerator.GetNewsArticle_AllMediaCompany(True,skipCondition,PostProcessing)
    return data_dict