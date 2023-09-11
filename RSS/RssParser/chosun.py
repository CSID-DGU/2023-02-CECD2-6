import requests
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
import re
import json

'''
    _ParseJson: 조선일보 본문에 사용되는 content Dictonary를 입력받아 실제 본문의 내용을 추출하는 함수
    입력: Json형태의 문자열 => {"content_elements",[]} 구조임을 확인함
    출력: [sentence1,sentence2,sentence3,sentence4] 구조의 List => 실제 본문내용
'''
def _ParseJson(jsonContext):
    json_data = jsonContext

    parsedJson = json.loads(json_data)
    content_elements = parsedJson.get('content_elements', [])

    combined_content = ""

    for element in content_elements:
        if element.get('type') == 'text':
            combined_content += element.get('content', '') + " "

    retList=re.split('(\. )',combined_content.strip())
    retList = ["".join(x) for x in zip(retList[::2], retList[1::2])]
    return retList

'''
    _ParseRssXML: 받은 Rss링크로 기사제목과 링크 List를 반환하는 함수
    입력: rssLink
    출력: [{"title"=title,"link"=link}] 구조의 List
'''
def _ParseRssXML(rssLink):
    retList=[]

    rssXml=requests.get(rssLink)
    parsedXml=ET.fromstring(rssXml.content)

    for item in parsedXml.findall('.//item'):
        title = item.find('title').text
        link = item.find('link').text
        retList.append({'title':title,'link':link})

    return retList

'''
    _ParseRssHTML: 받은 뉴스링크로 본문의 내용을 반환하는 함수
    입력: htmlLink
    출력: [sentence1,sentence2,sentence3,sentence4] 구조의 List
'''
def _ParseRssHTML(htmlLink):
    newsHtml=requests.get(htmlLink)
    soup = BeautifulSoup(newsHtml.text, 'html.parser')
    scriptTag=soup.find('script', {'id': 'fusion-metadata', 'type': 'application/javascript'})
    scriptText = scriptTag.string
    match = re.search(r'Fusion\.globalContent\s*=\s*(\{.*?\});', scriptText)

    if(match):
        fusion_global_content = match.group(1)
        return _ParseJson(fusion_global_content)
    else:
        return None

'''
    GetNewsArticles: 받은 주제:RssLink 쌍들로 부터 뉴스정보들을 가져오는 함수
    입력: {"주제이름1":"RssLink1","주제이름2":"RssLink2",...} 구조의 Dictionary
    출력: {"주제이름1":[{"title":title,"link"=link,"context":[sentence1,...]}...], ... } 구조의 List
'''
def GetNewsArticles(topicDict):
    retDicts={}
    for topicName in topicDict.keys():
        print('\tSet NewsTopic: '+topicName)
        retDicts[topicName]=[]
        
        rssLink=topicDict[topicName]
        newsDict=_ParseRssXML(rssLink)

        for news in newsDict:
            newsTitle=news['title']
            newsLink=news['link']
            print('\t\tStart Scrap News: '+newsTitle)
            newsContexts=_ParseRssHTML(newsLink)
            retDicts[topicName].append({'title':newsTitle,'link':newsLink,'context':newsContexts})
    return retDicts