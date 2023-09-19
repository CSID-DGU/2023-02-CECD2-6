from textrank.textrank.summarizer import KeywordSummarizer
from konlpy.tag import Okt, Komoran, Kkma
from re import split
import sys
import time

text = """
삼성·LG 가전이 전원 제어 중심의 단순 연동을 넘어 하나의 플랫폼으로 타사 가전 에너지 사용량 관리·절감이 가능한 서비스를 구현한다.
고객에게 비용 측면의 실질 혜택을 주는 동시에 제조사 수익모델까지 제시, 열린 스마트홈 생태계를 앞당길 전망이다.
글로벌 가전협의체 홈커넥티비티얼라이언스(HCA)는 독일 베를린에서 열린 IFA 2023 현장에서 전자신문과 그룹인터뷰를 갖고 이같이 밝혔다.
HCA는 지난해 1월 발족한 협의체로 삼성전자와 LG전자, 일렉트로룩스, 하이얼 등 15개 국내외 업체가 참여했다. 
삼성전자가 대표 의장, LG전자가 의장사로 활동 중이다.
HCA는 지난달 29일 IFA 2023 개막을 앞두고 삼성전자, LG전자, 베스텔(튀르키예) 등 간 가전 연동 계획을 알린데 이어 전시회 현장에서 관련 기술을 소개했다.
올해 1월 발표한 HCA 1.0의 첫 성과다.
1.0 버전은 회원사 가전 상호 연동을 통한 전원과 주요 모드 설정 제어가 핵심이다.
HCA는 IFA 2023에서 선보인 스마트홈 서비스에서 나아가 내년 HCA 2.0 표준을 공개할 계획이다.
발표 장소는 1월 초 미국 라스베이거스에서 열리는 세계 최대 가전·전자 전시회 CES 2024다.
HCA 2.0은 기존 버전에서 로봇청소기, 전기차 충전기 등을 적용 대상으로 추가한다.
주요 기능 역시 에너지 모니터링·관리를 새롭게 포함한다.
새 버전으로 업데이트하면 서로 다른 제조사 제품이라도 하나의 플랫폼 안에서 가전 에너지 사용량, 사용 데이터 분석 등이 가능하다.
추후 제조사별 인공지능(AI) 에너지 저감 모드 등을 지원할 경우 이 기능도 플랫폼 구분 없이 사용할 수 있다.
전기차 충전기와 연동해 집안에서도 가전기기를 이용해 충전 상태를 살필 수 있다.
에너지 관리는 최근 스마트홈 시장에서 관심이 집중되는 영역이다.
단순 편의를 넘어 고객에게 실질적인 혜택을 줄 수 있는 스마트홈 서비스 요구가 커지고 있다.
삼성전자와 LG전자도 각각 '스마트싱스' 'LG씽큐'를 통해 가전 에너지 사용량 모니터링, 최적 사용 모드 지원 등을 제공 중이다.
HCA 2.0을 적용하면 삼성 스마트싱스로 LG전자 가전의 에너지 사용량까지 모니터링, 에너지 관리 범위를 확장할 수 있다.
가전 연동에는 터키 베스텔도 참여했다.
셀라하틴 콕살 베스텔 IoT 전략팀장은 “다양한 스마트홈 서비스 중에서도 표준을 활용한 전기차 충전과 에너지 저장, 관리 부문 서비스 고도화에 초점을 맞추고 있다”고 말했다.
HCA는 내년 1월 2.0 버전 공개와 함께 일부 제품 시연도 검토 중이다.
이를 바탕으로 이르면 상반기 삼성전자, LG전자 등부터 적용을 추진한다.
대상 제품은 세탁기, 냉장고, 에어컨, TV 등 전력 소모가 큰 제품이 우선일 가능성이 높다.
최윤호 HCA 의장은 “2.0 표준은 사용자에게 비용절감과 같은 실질적인 혜택을 주는 동시에 스마트홈 서비스 사업화를 구현할 수 있다는 점에서 의미가 크다”며 “가전, 에너지, 충전 솔루션 회사가 협업해 새로운 시장을 만들 수 있을 것”이라고 말했다.
"""

# RSS로 받을 때 미리 전처리해서 한 문장씩 받아올 수 있으면 처리가 쉬울듯
text = text.split("\n")
sents = [sent.strip() for sent in text if len(sent) != 0]
# print(sents)


okt = Okt()
def okt_tokenize(sent):
    words = sent.split()
    words = okt.pos(sent, join=True)
    words = [w for w in words if ('/Noun' in w or '/Adjective' in w or '/Verb' in w)]
    # print(words)
    return words

komoran = Komoran()
def komoran_tokenize(sent):
    words = sent.split()
    words = komoran.pos(sent, join=True)
    words = [w for w in words if (('/NN' in w and '/NNB' not in w) or '/XR' in w or '/VA' in w or '/VV' in w)]
    # print(words)
    return words

kkma = Kkma()
def kkma_tokenize(sent):
    words = sent.split()
    words = kkma.pos(sent, join=True)
    words = [w for w in words if (('/NN' in w and '/NNB' not in w) or '/XR' in w or '/VA' in w or '/VV' in w)]
    return words

def TextRank(text: list, topk: int=5):
    sents = [sent.strip() for sent in text if len(sent) != 0]
    
    keyword_extractor = KeywordSummarizer(
        tokenize=komoran_tokenize,
        window = -1,
        verbose = False
    )

    keywords = keyword_extractor.summarize(sents, topk)

    words = []
    for word, rank in keywords:
        words.append(word.split("/")[0])

    return words
