from oai_content_generation import OaiContentGenerator

def main():
    # Initialize the content generator
    generator = OaiContentGenerator(model_name="gpt-3.5-turbo")

    # 1. AI Keywords Generation
    ai_keywords = generator.GenerateKeywords(topic="FinTech startups")

    # Validate and clean the keyword list
    if not ai_keywords or not isinstance(ai_keywords, list):
        print("Error: No keywords generated.")
        return

    ai_keywords = [kw.strip() for kw in ai_keywords]  # Clean spaces

    # 2. Content Generation
    generated_post = []
    for keyword in ai_keywords:
        post = generator.GenerateBlogPost(keyword=keyword)
        generated_post.append(post)

    seo_optimized_posts = []
    # 3. SEO Optimization
    for post in generated_post:
        improved_seo = generator.ReviewAndImproveSEO(post)
        seo_optimized_posts.append(improved_seo)

    # Print the final output safely
    if seo_optimized_posts:
        print("Final Blog Post:\n", seo_optimized_posts[0])
    else:
        print("No blog posts were generated successfully.")

if __name__ == "__main__":
   main()
