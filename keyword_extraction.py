''' Module to extract trending keywords from Google Trends and preprocess them, and to generate keywords for a given topic using
AI and Google search results'''

# Importing from this application's modules
from oai_content_generation import OaiContentGenerator

# Importing from external libraries
from googlesearch import search
from collections import Counter
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
import requests
import nltk
import re
import concurrent.futures
import random

# Download NLTK stopwords once
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')
stop_words = set(stopwords.words('english'))



class GoogleScraper:
    ''' Class to scrape Google search results and extract most common keywords from the search results'''

    def __init__(self):
        pass
    
    def get_google_search_results(self, topic: str = "FinTech", num_results = 10):
        ''' Get Google search results links for a given topic'''

        results = []
        try:
            for url in search(topic, num_results=num_results, unique=True):
                results.append(url)
        except Exception as e:
            print(f"Error fetching search results: {e}")
        return results
    
    def scrape_keywords_from_url(self, url):
        ''' Scrape title, headings, and meta description from a given URL'''

        try:
            response = requests.get(url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
            soup = BeautifulSoup(response.text, 'html.parser')
            title = soup.title.string if soup.title else ""
            headings = [h.get_text() for h in soup.find_all(['h1', 'h2', 'h3'])]
            meta_description = soup.find('meta', attrs={'name': 'description'})
            meta_description = meta_description['content'] if meta_description else ""
            return {"title": title, "headings": headings, "meta_description": meta_description}
        except Exception as e:
            print(f"Error scraping {url}: {e}")
            return None
    
    def extract_keywords(self, text, num_keywords=50):
        ''' Extract most common keywords from text'''

        stop_words = set(stopwords.words('english'))
        words = re.findall(r'\b\w+\b', text.lower())
        words = [word for word in words if word not in stop_words and len(word) > 2]
        return Counter(words).most_common(num_keywords)

    def get_keywords_from_google(self, topic, num_results=10, num_keywords=50):
        ''' Get most common keywords from Google search results for a given topic'''

        urls = self.get_google_search_results(topic, num_results)
        extracted_data = []
        
        # Scrape each URL in parallel
        with concurrent.futures.ThreadPoolExecutor() as executor:
            results = list(executor.map(self.scrape_keywords_from_url, urls))
        
        # Extract keywords from each URL
        for data in results:
            if data:
                extracted_data.append(data)
        if not extracted_data:
            print("No data extracted from search results.")
            return []

        # Combine all text from titles, headings, and meta descriptions
        all_text = " ".join([
            data['title'] + " " + " ".join(data['headings']) + " " + data['meta_description']
            for data in extracted_data
        ])
        return self.extract_keywords(all_text, num_keywords)


class KeywordGeneration:
    ''' Class to generate keywords for a given topic using AI and Google search results'''

    def __init__(self):
        pass

    def generate_keywords(self, topic: str, generation_model:str, num_keywords:int, num_google_keywords:int = 20, num_google_results:int = 50) -> tuple[list[list[str]],list[list[str]],list[list[str]]]:
        ''' Generate keywords for a given topic using AI and Google search results'''

        generator = OaiContentGenerator(model_name=generation_model)
        
        # Generate first set of keywords using AI
        ai_only_keywords = generator.GenerateKeywords(topic=topic)
        if not ai_only_keywords or not isinstance(ai_only_keywords, list):
            print("Error: No keywords generated.")
            ai_only_keywords = []
        for i,kw_sublist in enumerate(ai_only_keywords):
            ai_only_keywords[i] = [kw.strip() for kw in kw_sublist]
        

        # Generate second set of keywords using web scraping
        scraper = GoogleScraper()
        keywords = scraper.get_keywords_from_google(topic, num_results=num_google_results, num_keywords=num_google_keywords)
        google_and_ai_keywords = generator.GenerateKeywordsFromSearchResults(search_results=keywords, topic=topic)
        if not google_and_ai_keywords or not isinstance(google_and_ai_keywords, list):
            print("Error: No keywords generated.")
            google_and_ai_keywords = []
        for i,kw_sublist in enumerate(google_and_ai_keywords):
            google_and_ai_keywords[i] = [kw.strip() for kw in kw_sublist]
        
        # Combine and shuffle keywords
        final_keywords = ai_only_keywords + google_and_ai_keywords
        random.shuffle(final_keywords)
        if len(final_keywords) > num_keywords:
            final_keywords = final_keywords[:num_keywords]
        else:
            print(f"Warning: Only {len(final_keywords)} keywords generated.")

        return final_keywords, ai_only_keywords, google_and_ai_keywords