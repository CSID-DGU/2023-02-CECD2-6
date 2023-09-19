import sys
import json
from importlib import import_module

sys.path.append('./RSS/RssParser')

_jsonData ={}

'''
    _LoadConfigFile: rssConfig.json의 내용을 파싱
'''
def _LoadConfigFile():
    with open('./RSS/rssConfig.json', 'r', encoding='utf-8') as f:
        global _jsonData
        _jsonData = json.load(f)

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
    _LoadConfigFile()

    retDict={}
    for companyNameENG in _jsonData.keys():
        if(printOption):
            print('Start: _GetNewsArticle_Company['+companyNameENG+']')
            
        retDict[companyNameENG]={}
        retDict[companyNameENG]['companyName']=_jsonData[companyNameENG]['companyName']
        retDict[companyNameENG]['articles']=_GetNewsArticle_Company(companyNameENG,printOption,skipCondition)

        if(printOption):
            print('End: _GetNewsArticle_Company['+companyNameENG+']')
    
    if(postProcessFunc is not None):
        postProcessFunc(retDict)
    
    return retDict