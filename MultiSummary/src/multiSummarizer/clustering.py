from konlpy.tag import Komoran
from gensim import corpora 

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import Normalizer

from sklearn.cluster import AgglomerativeClustering
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import matplotlib.pyplot as plt
from sklearn.metrics import adjusted_rand_score, silhouette_score, davies_bouldin_score, calinski_harabasz_score
from sklearn.metrics.pairwise import cosine_similarity

from itertools import combinations

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
    
    def silhouette_analysis(self, max_k):
        article_without_newlines=self.make_article_without_newlines()
        #tf-idf 임베딩(+Normalize)
        tfidf_vectorizer = TfidfVectorizer(min_df = 3, ngram_range=(1,5))
        tfidf_vectorizer.fit(article_without_newlines)
        vector = tfidf_vectorizer.transform(article_without_newlines).toarray()

        normalizer = Normalizer()
        vector = normalizer.fit_transform(vector)
    
        silhouette_scores = []
        try:
            for k in range(2, max_k + 1):
                kmeans = KMeans(n_clusters=k,n_init='auto', random_state=42)
                labels = kmeans.fit_predict(vector)
                silhouette_avg = silhouette_score(vector, labels)
                silhouette_scores.append(silhouette_avg)
        except: 
            return similar_sentence_groups(article_without_newlines)
        
        # Find the optimal K based on Silhouette Score
        optimal_k = np.argmax(silhouette_scores) + 2  # +2 because the loop starts from k=2

        # K-means clustering with the optimal K
        kmeans_optimal = KMeans(n_clusters=optimal_k, random_state=42)
        labels_optimal = kmeans_optimal.fit_predict(vector)

        # Organize sentences into clusters
        clustered_sentences = [[] for _ in range(optimal_k)]
        for i in range(optimal_k):
            clustered_sentences[i] = list(np.array(article_without_newlines)[labels_optimal == i])

        article_clusters = {}
        # 주제별로 클러스터링된 인덱스를 사용하여 기사들을 그룹화
        for indices,topic in enumerate(clustered_sentences):
            article_clusters[indices] = topic

        return article_clusters
    
    def silhouette_analysis_with_score(self, max_k):
        article_without_newlines=self.make_article_without_newlines()
        #tf-idf 임베딩(+Normalize)
        tfidf_vectorizer = TfidfVectorizer(min_df = 3, ngram_range=(1,5))
        tfidf_vectorizer.fit(article_without_newlines)
        vector = tfidf_vectorizer.transform(article_without_newlines).toarray()

        normalizer = Normalizer()
        vector = normalizer.fit_transform(vector)
    
        silhouette_scores = []
        try:
            for k in range(2, max_k + 1):
                kmeans = KMeans(n_clusters=k, random_state=42)
                labels = kmeans.fit_predict(vector)
                silhouette_avg = silhouette_score(vector, labels)
                silhouette_scores.append(silhouette_avg)
        except: 
            print(article_without_newlines)
            print(calculate_cosine_similarity(article_without_newlines[0],article_without_newlines[1]))
        
        # Find the optimal K based on Silhouette Score
        optimal_k = np.argmax(silhouette_scores) + 2  # +2 because the loop starts from k=2
        print(f"Optimal K based on Silhouette Score: {optimal_k}")

        # K-means clustering with the optimal K
        kmeans_optimal = KMeans(n_clusters=optimal_k, random_state=42)
        labels_optimal = kmeans_optimal.fit_predict(vector)

        # Output clustering results
        for i in range(optimal_k):
            cluster_sentences = np.array(article_without_newlines)[labels_optimal == i]
            print(f"Cluster {i + 1}:")
            print(cluster_sentences)
            print("\n")

        # Plotting Silhouette Score
        plt.plot(range(2, max_k + 1), silhouette_scores, marker='o')
        plt.title('Silhouette Score Analysis')
        plt.xlabel('Number of clusters (K)')
        plt.ylabel('Silhouette Score')
        plt.show()

        # Simulated true labels (replace with actual labels if available)
        true_labels = np.zeros(len(article_without_newlines))
        # Silhouette Score
        silhouette_avg = silhouette_score(vector, labels)
        print(f"Silhouette Score for K={k}: {silhouette_avg}")
        # Davies-Bouldin Index
        db_index = davies_bouldin_score(vector, labels)
        print(f"Davies-Bouldin Index for K={k}: {db_index}")
        # Calinski-Harabasz Index
        ch_index = calinski_harabasz_score(vector, labels)
        print(f"Calinski-Harabasz Index for K={k}: {ch_index}")

        # Organize sentences into clusters
        clustered_sentences = [[] for _ in range(optimal_k)]
        for i in range(optimal_k):
            clustered_sentences[i] = list(np.array(article_without_newlines)[labels_optimal == i])

        article_clusters = {}
        # 주제별로 클러스터링된 인덱스를 사용하여 기사들을 그룹화
        for indices,topic in enumerate(clustered_sentences):
            article_clusters[indices] = topic

        return article_clusters
    
def calculate_cosine_similarity(sentences1, sentences2):
    # TfidfVectorizer를 사용하여 문장들을 TF-IDF 벡터로 변환
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([sentences1, sentences2])

    # 코사인 유사도 계산
    cosine_similarities = cosine_similarity(tfidf_matrix)[0][1]

    return cosine_similarities

def similar_sentence_groups(news):
    # 그룹별로 유사한 문장들을 저장할 딕셔너리
    similar_sentence_groups = {}
    similar_sentence_groups[0]=[news[0]]

    # 임계값 설정
    threshold = 0.5

    for sentence in news[1:]:
        for key, group in similar_sentence_groups.items():
            for exist_sentence in group:
                if calculate_cosine_similarity(exist_sentence, sentence) > threshold:
                    # 이미 있는 그룹에 추가
                    group.append(sentence)
                    found_group = True
                    break

        # 유사한 그룹이 없으면 새로운 그룹 생성
        if not found_group:
            similar_sentence_groups[len(similar_sentence_groups)] = [sentence]

        found_group = False

    return similar_sentence_groups