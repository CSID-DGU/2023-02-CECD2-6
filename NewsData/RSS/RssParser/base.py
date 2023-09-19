'''
    _ParseRssXML: 받은 Rss링크로 기사제목과 링크 List를 반환하는 함수
    입력: rssLink
    출력: [{"title"=title,"link"=link}] 구조의 List
'''
def _ParseRssXML(link):
    pass

'''
    _ParseRssHTML: 받은 뉴스링크로 본문의 내용을 반환하는 함수
    입력: htmlLink
    출력: [sentence1,sentence2,sentence3,sentence4] 구조의 List
'''
def _ParseRssHTML(link):
    pass

'''
    GetNewsArticles: 받은 주제:RssLink 쌍들로 부터 뉴스정보들을 가져오는 함수
    입력: {"주제이름1":"RssLink1","주제이름2":"RssLink2",...} 구조의 Dictionary, 진행상황 출력 여부, 뉴스기사 생략 조건
    출력: {"주제이름1":[{"title":title,"link"=link,"context":[sentence1,...]}...], ... } 구조의 List
'''
def GetNewsArticles(topicDict,printOption,skipCondition):
    retDicts={}
    for topicName in topicDict.keys():
        if(printOption):
            print('\tSet NewsTopic: '+topicName)

        retDicts[topicName]=[]
        
        rssLink=topicDict[topicName]
        newsDict=_ParseRssXML(rssLink)

        for news in newsDict:
            # 생략 조건에 맞는 뉴스는 크롤링을 하지 않는다.
            if(skipCondition is not None and skipCondition(news)):
                continue

            newsTitle=news['title']
            newsLink=news['link']
            
            if(printOption):
                print('\t\tStart Scrap News: '+newsTitle)

            newsContexts=_ParseRssHTML(newsLink)
            retDicts[topicName].append({'title':newsTitle,'link':newsLink,'context':newsContexts})
    return retDicts