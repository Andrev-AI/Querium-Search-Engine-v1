import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
from collections import defaultdict
import math
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import networkx as nx
import json
import random
from fake_useragent import UserAgent
from requests.exceptions import RequestException

nltk.download('punkt')
nltk.download('stopwords')

class Crawler:
    def __init__(self, max_pages=100, max_depth=3):
        self.max_pages = max_pages
        self.max_depth = max_depth
        self.visited = set()
        self.to_visit = []
        self.pages = {}
        self.ua = UserAgent()
        self.proxies = self.load_proxies()

    def load_proxies(self):
        # This is a placeholder. In a real scenario, you'd load a list of proxies from a file or service.
        return [
            'http://proxy1.example.com:8080',
            'http://proxy2.example.com:8080',
            'http://proxy3.example.com:8080'
        ]

    def get_random_headers(self):
        return {
            
        }

    def crawl(self, start_urls):
        self.to_visit = [(url, 0) for url in start_urls]
        
        while self.to_visit and len(self.visited) < self.max_pages:
            url, depth = self.to_visit.pop(0)
            
            if url not in self.visited and depth <= self.max_depth:
                print(f"Crawling: {url}")
                self.visit_page(url, depth)

        self.calculate_page_rank()

    def visit_page(self, url, depth):
        headers = self.get_random_headers()
        proxy = random.choice(self.proxies)

        try:
            response = self.make_request(url, headers, proxy)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                text = self.extract_text(soup)
                title = soup.title.string if soup.title else ''
                
                self.pages[url] = {
                    'url': url,
                    'title': title,
                    'text': text,
                }
                
                self.visited.add(url)
                
                if depth < self.max_depth:
                    new_links = self.extract_links(url, soup)
                    self.links[url].update(new_links)
                    self.to_visit.extend((link, depth + 1) for link in new_links 
                                         if link not in self.visited)
            else:
                print(f"Failed to crawl {url}: Status code {response.status_code}")
                
        except Exception as e:
            print(f"Error crawling {url}: {str(e)}")

    def make_request(self, url, headers, proxy):
        try:
            response = requests.get(url, headers=headers, proxies={'http': proxy, 'https': proxy}, timeout=10)
            if response.status_code == 403:  # Forbidden
                print(f"Access forbidden. Retrying with different proxy and user agent.")
                headers = self.get_random_headers()
                proxy = random.choice(self.proxies)
                response = requests.get(url, headers=headers, proxies={'http': proxy, 'https': proxy}, timeout=10)
            return response
        except RequestException as e:
            print(f"Request failed: {str(e)}. Retrying with different proxy.")
            proxy = random.choice(self.proxies)
            return requests.get(url, headers=headers, proxies={'http': proxy, 'https': proxy}, timeout=10)

    def extract_text(self, soup):
        for script in soup(["script", "style"]):
            script.decompose()
        
        text = soup.get_text()
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = ' '.join(chunk for chunk in chunks if chunk)
        
        return text

    def extract_links(self, base_url, soup):
        links = set()
        for a_tag in soup.find_all('a', href=True):
            link = urljoin(base_url, a_tag['href'])
            if self.is_valid_url(link):
                links.add(link)
        return links

    def is_valid_url(self, url):
        parsed = urlparse(url)
        return bool(parsed.netloc) and bool(parsed.scheme)

    def calculate_page_rank(self):
        G = nx.DiGraph(self.links)
        page_ranks = nx.pagerank(G)
        for url in self.pages:
            self.pages[url]['page_rank'] = page_ranks.get(url, 0.85)  # Default value if not in pagerank results

class AdvancedIndexer:
    def __init__(self):
        self.inverted_index = defaultdict(list)
        self.document_vectors = {}
        self.idf = {}
        self.total_documents = 0
        self.stemmer = PorterStemmer()
        self.stop_words = set(stopwords.words('english') + stopwords.words('portuguese'))
        self.page_ranks = {}
        self.avg_doc_length = 0

    def preprocess(self, text):
        tokens = word_tokenize(text.lower())
        return [self.stemmer.stem(token) for token in tokens 
                if token.isalnum() and token not in self.stop_words]

    def add_document(self, doc_id, title, text, page_rank):
        tokens = self.preprocess(title + " " + text)
        self.total_documents += 1
        
        term_freq = defaultdict(int)
        for token in tokens:
            term_freq[token] += 1
        
        doc_vector = {}
        for term, freq in term_freq.items():
            self.inverted_index[term].append((doc_id, freq))
            doc_vector[term] = freq
        
        self.document_vectors[doc_id] = doc_vector
        self.page_ranks[doc_id] = page_rank
        self.avg_doc_length += len(tokens)

    def calculate_idf(self):
        self.avg_doc_length /= self.total_documents
        for term, postings in self.inverted_index.items():
            self.idf[term] = math.log((self.total_documents - len(postings) + 0.5) / (len(postings) + 0.5) + 1)

    def index_documents(self, documents):
        for doc_id, doc in documents.items():
            self.add_document(doc_id, doc['title'], doc['text'], doc['page_rank'])
        self.calculate_idf()

    def save_index(self, filename):
        index_data = {
            'inverted_index': dict(self.inverted_index),
            'document_vectors': self.document_vectors,
            'idf': self.idf,
            'total_documents': self.total_documents,
            'page_ranks': self.page_ranks,
            'avg_doc_length': self.avg_doc_length
        }
        with open(filename, 'w') as f:
            json.dump(index_data, f)

    def load_index(self, filename):
        with open(filename, 'r') as f:
            index_data = json.load(f)
        self.inverted_index = defaultdict(list, index_data['inverted_index'])
        self.document_vectors = index_data['document_vectors']
        self.idf = index_data['idf']
        self.total_documents = index_data['total_documents']
        self.page_ranks = index_data['page_ranks']
        self.avg_doc_length = index_data['avg_doc_length']


if __name__ == "__main__":
    # Initialize and run the crawler
    crawler = Crawler(max_pages=100, max_depth=10)
    start_urls = ['https://www.example.com.']
    crawler.crawl(start_urls)

    # Initialize and run the indexer
    indexer = AdvancedIndexer()
    indexer.index_documents(crawler.pages)

    # Save the index
    indexer.save_index('querium_alexandrya.json')
    print("Index saved successfully.")