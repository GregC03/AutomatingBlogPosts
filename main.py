from oai_content_generation import OaiContentGenerator, OaiSeoSpecialist
from keyword_extraction import GoogleScraper
from seo_optimization import SEOAnalyzer

import random
import pandas as pd
import openpyxl

def main(topic: str, input_keywords: list = None):
    ''' Main function to generate SEO-optimized blog posts on a given topic'''

    # 1a. If input_keywords are not provided, generate keywords using AI and web scraping
    if input_keywords is None:
        
        generator = OaiContentGenerator(model_name="gpt-3.5-turbo")
        keywords = ["Innovative payments", "payment solutions", "digital payments", "payment technology", "payment innovation"]

        ## AI Keywords Generation from scratch
        ai_keywords1 = generator.GenerateKeywords(topic=topic)

        ### Validate and clean the keyword list
        if not ai_keywords1 or not isinstance(ai_keywords1, list):
            print("Error: No keywords generated.")
            ai_keywords1 = []

        ### Clean spaces
        ai_keywords1 = [kw.strip() for kw in ai_keywords1]

        ## Keyword extraction from web-scraping
        scraper = GoogleScraper()
        
        ### Get common  keywords related to a topic from Google search results
        keywords = scraper.get_keywords_from_google(topic, num_results=50, num_keywords=20)

        ### Pass the extracted_keywords to the AI model
        ai_keywords2 = generator.GenerateKeywordsFromSearchResults(search_results=keywords, topic=topic)

        ### Validate and clean the keyword list
        if not ai_keywords1 or not isinstance(ai_keywords1, list):
            print("Error: No keywords generated.")
            ai_keywords1 = []

        ### Clean spaces
        ai_keywords2 = [kw.strip() for kw in ai_keywords2]

        ## Combine the keywords
        final_keywords = list(set(ai_keywords1 + ai_keywords2))
        random.shuffle(final_keywords)
        #if len(final_keywords) > 700//30:
        #    final_keywords = final_keywords[:700//30]
        final_keywords = final_keywords[:5]

    # 1b. If input_keywords are provided, use them directly
    else:
        final_keywords = input_keywords

    #######################################################################################################################

    # 2. Content Generation
    generated_posts = []
    generated_titles = []
    generated_metadescriptions = []
    for keyword in final_keywords:
        post = generator.GenerateBlogPost(keyword=keyword)
        title = generator.GeneratePostTitle(blog_text=post, keyword=keyword)
        metadescription = generator.GeneratePostMetaDescription(blog_text=post, blog_title=title, keyword=keyword)
        post = title + "\n" + metadescription + "\n" + post
        generated_posts.append(post)
        generated_titles.append(title)
        generated_metadescriptions.append(metadescription)

    #######################################################################################################################

    # 3. SEO Optimization

    ## Initialize the SEO Analyzer and SEO Specialist
    analyzer = SEOAnalyzer()
    fixer = OaiSeoSpecialist(model_name="gpt-3.5-turbo")

    ## Optimize the generated blog posts
    seo_optimized_posts = []

    for i,post in enumerate(generated_posts):
        existing_contents = generated_posts[:i]+generated_posts[i+1:]
        corrections = analyzer.generate_report(content=post, target_keywords=final_keywords[i], title=generated_titles[i], meta_description=generated_metadescriptions[i], existing_contents=existing_contents)
        improved_post = fixer.FixBlogPost(post, corrections)
        seo_optimized_posts.append(improved_post)


    ## Warn if no blog posts were generated successfully
    if not seo_optimized_posts:
        print("No blog posts were generated successfully.")

    # Create a DataFrame with the blog posts
    df = pd.DataFrame({
        'blog_post': seo_optimized_posts,
        'keyword': final_keywords
    })

    # Save to CSV and Excel
    try:
        df.to_csv('./automated_blog_posts.csv', index=False, sep=';')
        df.to_excel('./automated_blog_posts.xlsx', index=False, engine='openpyxl')
        print("Files saved successfully.")
    except PermissionError:
        print("Error: Permission denied. Please close the files if they are open.")
    except Exception as e:
        print(f"Error saving files: {str(e)}")

    return seo_optimized_posts

if __name__ == "__main__":
   main(topic = "Innovative payments solutions")