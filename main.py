'''The main script to generate SEO-optimized blog posts on a given topic using AI and web scraping,
add content linking, and publish to a CMS like WordPress.'''

# Importing from this application's modules
from oai_content_generation import ContentGeneration
from keyword_extraction import KeywordGeneration
from seo_optimization import SEOFixer
from cms_integration import CMSIntegration
#from internal_linking import InternalLinking

# Importing from external libraries
import pandas as pd
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Main function to generate and publish SEO-optimized blog posts on a given topic
def main(topic: str, input_keywords: list = None):
    """Main function to generate SEO-optimized blog posts on a given topic.
    
    Args:
        topic (str): The main topic for blog post generation
        input_keywords (list, optional): List of keywords to use. If None, generates keywords automatically
    
    Returns:
        list: List of SEO-optimized blog posts
    """
    generation_model = os.getenv("generation_model", "gpt-4o-mini")  # Model name for AI content generation


    # PHASE 1: KEYWORD GENERATION
    ## Either use provided keywords or generate new ones using AI and web scraping
    if input_keywords is None:
        keyword_generator = KeywordGeneration() # Class to generate keywords using AI and Google search results
        final_keywords, _, _ = keyword_generator.generate_keywords(
                                                    topic=topic,
                                                    generation_model=generation_model,
                                                    num_keywords = 4,
                                                    num_google_keywords=20,
                                                    num_google_results=50
                                                ) # Generate a list of (up to num_keywords) lists of semantically close keywords related to the topic using AI and Google search results
    
        ## Check if keywords were generated successfully
        if not final_keywords:
            raise ValueError("No keywords were generated successfully.")
    
    else:
        final_keywords = input_keywords


    # PHASE 2: CONTENT GENERATION
    ## Generate blog posts, titles, and meta descriptions for each keyword
    contentgen = ContentGeneration() # Class to generate blog posts, titles, and meta descriptions
    generated_posts, generated_titles, generated_metadescriptions = contentgen.Posts_Titles_Metadescriptions_Generator(
                                                                                                            generation_model,
                                                                                                            final_keywords
                                                                                                        ) # Generate blog posts, titles, and meta descriptions for each list of keywords
    
    ## Check if blog posts were generated successfully
    if not generated_posts:
        raise ValueError("No blog posts were generated successfully.")

    # PHASE 3: SEO OPTIMIZATION
    ## Analyze and improve each post for SEO
    seo_model = os.getenv("seo_model", "gpt-4o-mini") # Name of the AI Model for content generation
    
    ## Fix SEO issues in blog posts
    fixer = SEOFixer() # Class to fix SEO issues in blog posts
    seo_optimized_posts, seo_optimized_titles, seo_optimized_metadescriptions = fixer.fixSEO(
                                                                                        seo_model=seo_model,
                                                                                        generated_posts=generated_posts,
                                                                                        generated_titles=generated_titles,
                                                                                        generated_metadescriptions=generated_metadescriptions,
                                                                                        final_keywords=final_keywords
                                                                                    ) # Finds and fixes SEO issues in blog posts


    ## Check if seo optimized blog posts were generated successfully
    if not seo_optimized_posts:
        raise ValueError("No blog posts were generated successfully.")

    # PHASE 4: INTERNAL LINKING STRATEGY
    ## Generate internal links for SEO optimization
    ## TODO: Implement internal linking strategy

    # PHASE 5: SAVE RESULTS LOCALLY
    ## Save the generated posts to CSV and Excel files
    df = pd.DataFrame({
        'title': seo_optimized_titles,
        'meta_description': seo_optimized_metadescriptions,
        'blog_post': seo_optimized_posts,
        'keyword': final_keywords
    })
    try:
        df.to_csv('./automated_blog_posts.csv', index=False, sep=';')
        df.to_excel('./automated_blog_posts.xlsx', index=False, engine='openpyxl')
        print("Files saved successfully.")
    except PermissionError:
        print("Error: Permission denied. Please close the files if they are open.")
    except Exception as e:
        print(f"Error saving files: {str(e)}")

    ## Save the posts to a Word document keeping markdown formatting
    for i, post in enumerate(seo_optimized_posts):
        with open(f'./blog_post_{i}.md', 'w', encoding='utf-8') as f:
            f.write(f"{seo_optimized_titles[i]}\n\n")
            f.write(f"{seo_optimized_metadescriptions[i]}\n\n")
            f.write(post)
    print("Markdown files saved successfully.")

    # PHASE 6: CMS INTEGRATION
    ## Publish blog posts to WordPress CMS

    ## Initialize CMS integration
    cms = CMSIntegration() # Class to integrate with a Content Management System (CMS) like WordPress

    ## Get CMS settings from environment variables
    pubtlish_to_cms = os.getenv("publish_to_cms", "False").lower() # Set to True to publish to CMS
    cms_type = os.getenv("cms_type", "wordpress").lower() # Type of CMS to publish to

    ## Set to True to publish as drafts
    draft = False

    ## Publish to CMS if enabled
    if pubtlish_to_cms == "true":
        cms.cms_publication(
            seo_optimized_posts=seo_optimized_posts,
            seo_optimized_titles=seo_optimized_titles,
            seo_optimized_metadescriptions=seo_optimized_metadescriptions,
            final_keywords=final_keywords,
            cms_type=cms_type,
            draft=draft
        )

    return seo_optimized_titles, seo_optimized_metadescriptions,seo_optimized_posts, final_keywords

if __name__ == "__main__":
   main(topic = "bloackchain")
