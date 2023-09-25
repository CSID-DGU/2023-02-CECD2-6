import requests
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
import re
import json
import RSS.utils as utils

companyName='chosun'

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
    출력: [{"title"=title,"link"=link,"date":date}] 구조의 List
    > date의 형식은 '%Y-%m-%d %H:%M:%S'
'''
def _ParseRssXML(rssLink):
    retList=[]

    rssXml=requests.get(rssLink)
    parsedXml=ET.fromstring(rssXml.content)

    for item in parsedXml.findall('.//item'):
        title = item.find('title').text
        link = item.find('link').text
        date = item.find('pubDate').text

        date=utils.ConvertRFC2822(date)

        retList.append({'title':title,'link':link,'date':date})

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
    입력: {"주제이름1":"RssLink1","주제이름2":"RssLink2",...} 구조의 Dictionary, 진행상황 출력 여부, 뉴스기사 생략 조건
    출력: {"주제이름1":[{"title":title,"link"=link,"date"=date,"context":[sentence1,...]}...], ... } 구조의 List
'''
def GetNewsArticles(topicDict,printOption,skipCondition):
    retDicts={}
    for topicName in topicDict.keys():
        if(printOption):
            print('\tSet NewsTopic: '+topicName)

        retDicts[topicName]=[]
        
        rssLink=topicDict[topicName]
        try:
            newsDict=_ParseRssXML(rssLink)
        except Exception:
            continue

        for news in newsDict:
            newsTitle=news['title']
            newsLink=news['link']
            newsDate=news['date']
            
            # 생략 조건에 맞는 뉴스는 크롤링을 하지 않는다.
            if(skipCondition is not None and skipCondition(news,companyName,topicName)):
                if(printOption):
                    print('\t\t[Skip] Scrap News: '+newsTitle)
                continue

            if(printOption):
                print('\t\tStart Scrap News: '+newsTitle)

            try:
                newsContexts=_ParseRssHTML(newsLink)
            except Exception:
                continue

            retDicts[topicName].append({'title':newsTitle,'link':newsLink,'date':newsDate,'context':newsContexts})
    return retDicts