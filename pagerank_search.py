from collections import defaultdict
import math
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import json

from .crawler_indexer import *

class SearchEngine:
    def __init__(self):
        self.indexer = None
        self.stemmer = PorterStemmer()
        self.stop_words = set(stopwords.words('english') + stopwords.words('portuguese'))

    def load_index(self, filename):
        self.indexer = AdvancedIndexer()
        self.indexer.load_index(filename)

    def preprocess(self, text):
        tokens = word_tokenize(text.lower())
        return [self.stemmer.stem(token) for token in tokens 
                if token.isalnum() and token not in self.stop_words]

    def calculate_bm25(self, doc_id, term, k1=1.8, b=0.75):
        if term not in self.indexer.document_vectors[doc_id]:
            return 0
        tf = self.indexer.document_vectors[doc_id][term]
        doc_length = sum(self.indexer.document_vectors[doc_id].values())
        numerator = tf * (k1 + 1)
        denominator = tf + k1 * (1 - b + b * doc_length / self.indexer.avg_doc_length)
        return self.indexer.idf[term] * numerator / denominator

    def custom_score(self, bm25_score, page_rank, boost=1.0):
        return bm25_score * math.log(1 + page_rank) * boost

    def search(self, query, top_k=10, use_page_rank=True, field_boosts=None):
        if field_boosts is None:
            field_boosts = {'title': 4.0, 'body': 3.0, 'url': 1.0}
        
        query_vector = self.vectorize_query(query)
        scores = defaultdict(float)
        
        for term, query_weight in query_vector.items():
            if term in self.indexer.inverted_index:
                for doc_id, _ in self.indexer.inverted_index[term]:
                    bm25 = self.calculate_bm25(doc_id, term)
                    if use_page_rank:
                        score = self.custom_score(bm25, self.indexer.page_ranks[doc_id], boost=field_boosts.get('body', 2.0))
                    else:
                        score = bm25 * field_boosts.get('body', 2.0)
                    scores[doc_id] += query_weight * score
        
        return sorted(scores.items(), key=lambda x: x[1], reverse=True)[:top_k]

    def vectorize_query(self, query):
        tokens = self.preprocess(query)
        query_tf = defaultdict(int)
        for token in tokens:
            query_tf[token] += 1
        
        query_vector = {}
        for term, tf in query_tf.items():
            if term in self.indexer.idf:
                query_vector[term] = tf * self.indexer.idf[term]
        
        return query_vector

# Main execution for searching
if __name__ == "__main__":
    search_engine = SearchEngine()
    search_engine.load_index('querium_alexandrya.json')
    
    while True:
        query = input("Enter your search query (or 'quit' to exit): ")
        if query.lower() == 'quit':
            break
        
        results = search_engine.search(query)
        
        print(f"Results for '{query}':")
        for doc_id, score in results:
            print(f"Document: {doc_id}")
            print(f"Score: {score}")
            print(f"Title: {search_engine.indexer.document_vectors[doc_id]['title']}")
            print(f"URL: {doc_id}")
            print(f"PageRank: {search_engine.indexer.page_ranks[doc_id]}")
            print("---")