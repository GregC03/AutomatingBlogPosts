from pytrends.request import TrendReq
from oai_content_generation import OaiContentGenerator
from googlesearch import search
import requests
from bs4 import BeautifulSoup
import nltk
from nltk.corpus import stopwords
import re
from collections import Counter

# Download NLTK stopwords once
nltk.download('stopwords')
stop_words = set(stopwords.words('english'))


class GoogleScraper:
    ''' Class to scrape Google search results and extract most common keywords from the search results'''
    def __init__(self):
        pass
    
    def get_google_search_results(self, topic: str = "FinTech", num_results = 10):
        """Fetches top Google search results for the given topic."""
        results = []
        try:
            for url in search(topic, num_results=num_results, unique=True):
                results.append(url)
        except Exception as e:
            print(f"Error fetching search results: {e}")
        return results
    
    def scrape_keywords_from_url(self, url):
        """Scrapes title, headings, and meta descriptions from the given URL."""
        try:
            response = requests.get(url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
            soup = BeautifulSoup(response.text, 'html.parser')

            # Extract relevant content
            title = soup.title.string if soup.title else ""
            headings = [h.get_text() for h in soup.find_all(['h1', 'h2', 'h3'])]
            meta_description = soup.find('meta', attrs={'name': 'description'})
            meta_description = meta_description['content'] if meta_description else ""

            return {"title": title, "headings": headings, "meta_description": meta_description}
        except Exception as e:
            print(f"Error scraping {url}: {e}")
            return None
    
    def extract_keywords(self, text, num_keywords=50):
        """Processes the scraped text and extracts common keywords."""
        words = re.findall(r'\b\w+\b', text.lower())
        words = [word for word in words if word not in stop_words and len(word) > 2]
        
        # Get the most common keywords
        return Counter(words).most_common(num_keywords)

    def get_keywords_from_google(self, topic, num_results=10, num_keywords=50):
        """Combines all methods to extract keywords from Google search results."""
        urls = self.get_google_search_results(topic, num_results)
        extracted_data = []

        for url in urls:
            data = self.scrape_keywords_from_url(url)
            if data:
                extracted_data.append(data)

        if not extracted_data:
            print("No data extracted from search results.")
            return []

        # Combine extracted text data
        all_text = " ".join([
            data['title'] + " " + " ".join(data['headings']) + " " + data['meta_description']
            for data in extracted_data
        ])

        # Extract and return keywords
        return self.extract_keywords(all_text, num_keywords)



class KeywordExtractor:
    ''' Class to extract trending keywords from Google Trends and preprocess them'''
    def __init__(self):
        pass

    def get_trending_keywords(self, topic="FinTech"):
        try:
            pytrends = TrendReq(hl='en-US', tz=360, timeout=(10, 25))
            pytrends.build_payload([topic], timeframe='today 12-m')
            
            data = pytrends.related_queries()

            if not data or topic not in data or data[topic]['top'] is None:
                print(f"No trending data found for {topic}, generating keywords with OpenAI instead.")
                generator = OaiContentGenerator()
                return generator.GenerateKeywords(topic=topic)

            top_queries = data[topic]['top']
            return top_queries['topic'].tolist()

        except Exception as e:
            print(f"Error fetching Google Trends data: {e}, generating keywords with OpenAI instead.")
            generator = OaiContentGenerator()
            
            return generator.GenerateKeywords(topic=topic)

    def preprocess_keywords(self, keyword_list):
        cleaned_keywords = list(set([kw.lower().strip() for kw in keyword_list if kw]))
        return cleaned_keywords
    


