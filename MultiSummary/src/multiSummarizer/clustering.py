from konlpy.tag import Komoran
from gensim import corpora 

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import Normalizer

from sklearn.cluster import AgglomerativeClustering

class Custer:
    def __init__(self, documents):
        self.documents = documents
        
    
    def make_corpus(self):
        #tokenizer
        komoran = Komoran()
        tokenList=[]
        for article in self.documents:
            temp=[]
            for sentence in article:
                tokens = komoran.nouns(sentence)
                #tokens = komoran.morphs(sentence)
                temp.append(tokens)
            tokenList.append(temp)
        print(tokenList)

        #불용어 제거 
        with open('korean_stopwords.txt', 'r', encoding='utf-8') as f:
            stop_words = f.read().split("\n")
        stop_words = ['은','는', 'ㄴ','다','.',',','(',')']+stop_words    
        print(len(stop_words), stop_words[:10])

        result=[]
        for article in tokenList:
            for tokens in article:
                result.append([word for word in tokens if not word in stop_words])
        print(result)

        dictionary = corpora.Dictionary(result)                    # 사전 생성 (토큰화)
        print(dictionary)

        # 출현빈도가 적거나 자주 등장하는 단어는 제거
        #dictionary.filter_extremes(no_below=10, no_above=0.05)
        corpus = [dictionary.doc2bow(text) for text in result] 
        print('Number of unique tokens: %d' % len(dictionary))
        print('Number of documents: %d' % len(corpus))

        corpus = [dictionary.doc2bow(text) for text in result]     # 말뭉치 생성 (벡터화)
        print('corpus : {}'.format(corpus))
        return corpus
    
    def make_article_without_newlines(self):
        article_without_newlines=[' '.join([sentence.strip('"') for sentence in sublist]) for sublist in self.documents]
                
        #print(article_without_newlines)
        return article_without_newlines


    def hierachyClustering(self):
        article_without_newlines=self.make_article_without_newlines()
        #tf-idf 임베딩(+Normalize)
        tfidf_vectorizer = TfidfVectorizer(min_df = 3, ngram_range=(1,5))
        tfidf_vectorizer.fit(article_without_newlines)
        vector = tfidf_vectorizer.transform(article_without_newlines).toarray()

        normalizer = Normalizer()
        vector = normalizer.fit_transform(vector)

        #모델 선언 및 군집화
        model = AgglomerativeClustering(linkage="average",  # vector끼리 bottom-up 방식으로 병합
                                    distance_threshold = 0.75, # 기준치 미만인 경우 다른 군집으로 판단
                                    n_clusters=None, # 클러스터의 개수 지정X
                                    affinity="cosine", # cosine similarity 방식으로 벡터 비교
                                    compute_full_tree ="auto")
        result=model.fit_predict(vector) # 해당 벡터가 어디에 속하는지 판단

        #print(result)
        print('군집개수 :', result.max()+1)        

        # 클러스터에 속하는 인덱스들을 해당 주제로 그룹화
        topic_clusters = {}
        for idx, topic in enumerate(result):
            if topic not in topic_clusters:
                topic_clusters[topic] = []
            topic_clusters[topic].append(idx)
        
        # 결과를 저장할 딕셔너리
        article_clusters = {}

        # 주제별로 클러스터링된 인덱스를 사용하여 기사들을 그룹화
        for topic, indices in topic_clusters.items():
            article_clusters[topic] = [article_without_newlines[index] for index in indices]

        #print(topic_clusters)
        return article_clusters