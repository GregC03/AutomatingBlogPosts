from oai_content_generation import OaiContentGenerator
from keyword_extraction import GoogleScraper
import random

def main(topic: str, input_keywords: list = None):
    if input_keywords is None:
        # 0. Initialization
        generator = OaiContentGenerator(model_name="gpt-3.5-turbo")
        keywords = ["Innovative payments", "payment solutions", "digital payments", "payment technology", "payment innovation"]
        #######################################################################################################################

        # 1a. AI Keywords Generation from scratch
        ai_keywords1 = generator.GenerateKeywords(topic=topic)

        ## Validate and clean the keyword list
        if not ai_keywords1 or not isinstance(ai_keywords1, list):
            print("Error: No keywords generated.")
            ai_keywords1 = []

        ## Clean spaces
        ai_keywords1 = [kw.strip() for kw in ai_keywords1]

        # 1b. Keyword extraction from web-scraping
        scraper = GoogleScraper()
        
        ## Get common  keywords related to a topic from Google search results
        keywords = scraper.get_keywords_from_google(topic, num_results=50, num_keywords=20)

        ## Pass the extracted_keywords to the AI model
        ai_keywords2 = generator.GenerateKeywordsFromSearchResults(search_results=keywords, topic=topic)

        ## Validate and clean the keyword list
        if not ai_keywords1 or not isinstance(ai_keywords1, list):
            print("Error: No keywords generated.")
            ai_keywords1 = []

        ## Clean spaces
        ai_keywords2 = [kw.strip() for kw in ai_keywords2]

        # 1c. Combine the keywords
        final_keywords = list(set(ai_keywords1 + ai_keywords2))
        random.shuffle(final_keywords)
        #if len(final_keywords) > 700//30:
        #    final_keywords = final_keywords[:700//30]

    else:
        final_keywords = input_keywords

    #######################################################################################################################

    # 2. Content Generation
    generated_post = []
    for keyword in final_keywords:
        post = generator.GenerateBlogPost(keyword=keyword)
        generated_post.append(post)

    #######################################################################################################################

    # 3. SEO Optimization
    seo_optimized_posts = []

    for post in generated_post:
        improved_seo = generator.ReviewAndImproveSEO(post)
        seo_optimized_posts.append(improved_seo)

    ## Print the final output safely
    if seo_optimized_posts:
        print("Final Blog Post:\n", seo_optimized_posts[0])
    else:
        print("No blog posts were generated successfully.")

if __name__ == "__main__":
   main(topic = "Innovative payments solutions")