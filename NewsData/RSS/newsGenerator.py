import sys
import json
from importlib import import_module
import datetime
import RSS.utils as utils

sys.path.append(utils.getHomePath('NewsData/RSS/RssParser'))

_jsonData ={}
 
def _WriteLastPostJson(d):
    ret=utils.LoadJsonFile(utils.getHomePath('NewsData/RSS/lastPost.json'))
    if ret is None:
        ret={}

    for company in d.keys():
        if(ret.get(company) is None):
            ret[company]={}
            
        for topic in d[company]['articles'].keys():
            articles=d[company]['articles'][topic]
            dates=[article['date'] for article in articles]
            sortedDates=sorted(dates,reverse=True)
            
            if(len(sortedDates)!=0):
                ret[company][topic]=sortedDates[0]
            elif(ret[company].get(topic) is None):
                ret[company][topic]=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    with open(utils.getHomePath('NewsData/RSS/lastPost.json'), 'w', encoding='utf-8') as f:
        json.dump(ret, f,ensure_ascii=False)

'''
    _GetNewsArticle_Company: 입력된 언론사이름의 뉴스데이터를 가져온다.
    입력: rssConfig의 Key값으로 존재하는 언론사이름
    출력: {"주제이름1":[{"title":title,"link"=link,"context":[sentence1,...]}...], ... } 구조의 List
'''
def _GetNewsArticle_Company(company,printOption,skipCondition):
    importFileName = _jsonData[company]['importFileName']
    topicDict = _jsonData[company]['topic']
    parserModule = import_module(importFileName)
    return parserModule.GetNewsArticles(topicDict,printOption,skipCondition)

'''
    GetNewsArticle_AllMediaCompany: rssConfig.json에 등록된 언론사들의 뉴스데이터를 가져온다.
    입력: 진행상황 출력 여부, 뉴스기사 생략 조건, 후처리 함수
    출력:
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
def GetNewsArticle_AllMediaCompany(printOption=True,skipCondition=None,postProcessFunc=None):
    global _jsonData
    _jsonData=utils.LoadJsonFile(utils.getHomePath('NewsData/RSS/rssConfig.json'))

    retDict={}
    for companyNameENG in _jsonData.keys():
        if(printOption):
            print('Start: _GetNewsArticle_Company['+companyNameENG+']')
            
        retDict[companyNameENG]={}
        retDict[companyNameENG]['companyName']=_jsonData[companyNameENG]['companyName']
        retDict[companyNameENG]['articles']=_GetNewsArticle_Company(companyNameENG,printOption,skipCondition)

        if(printOption):
            print('End: _GetNewsArticle_Company['+companyNameENG+']')
    
    # 후처리
    if(postProcessFunc is not None):
        postProcessFunc(retDict)
    
    # 최신 기사 숫자입력
    _WriteLastPostJson(retDict)

    return retDict