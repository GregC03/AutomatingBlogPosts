class KeywordExtractorfromTrends:
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
    