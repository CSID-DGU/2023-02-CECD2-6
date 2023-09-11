import sys
import json
from importlib import import_module

sys.path.append('./RssParser')

_jsonData ={}

'''
    _LoadConfigFile: rssConfig.json의 내용을 파싱
'''
def _LoadConfigFile():
    with open('rssConfig.json', 'r', encoding='utf-8') as f:
        global _jsonData
        _jsonData = json.load(f)

'''
    _GetNewsArticle_Company: 입력된 언론사이름의 뉴스데이터를 가져온다.
    입력: rssConfig의 Key값으로 존재하는 언론사이름
    출력: {"주제이름1":[{"title":title,"link"=link,"context":[sentence1,...]}...], ... } 구조의 List
'''
def _GetNewsArticle_Company(company):
    importFileName = _jsonData[company]['importFileName']
    topicDict = _jsonData[company]['topic']
    parserModule = import_module(importFileName)
    return parserModule.GetNewsArticles(topicDict)

'''
    GetNewsArticle_AllMediaCompany: rssConfig.json에 등록된 언론사들의 뉴스데이터를 가져온다.
    입력: 중복기사 스크랩 여부, 진행상황 출력 여부
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
def GetNewsArticle_AllMediaCompany(skipOption=False,printOption=True):
    _LoadConfigFile()

    retDict={}
    for companyNameENG in _jsonData.keys():
        print('Start: _GetNewsArticle_Company['+companyNameENG+']')
        retDict[companyNameENG]={}
        retDict[companyNameENG]['companyName']=_jsonData[companyNameENG]['companyName']
        retDict[companyNameENG]['articles']=_GetNewsArticle_Company(companyNameENG)
        print('End: _GetNewsArticle_Company['+companyNameENG+']')
    
    return retDict