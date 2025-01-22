# main.py

from oai_content_generation import OaiContentGenerator
from seo_optimizer import SEOOptimizer

if __name__ == "__main__":
    keyword = "FinTech innovation in 2025"

    generator = OaiContentGenerator(model_name="EleutherAI/gpt-neo-1.3B", max_length=500)

    # 0. AI Keywords Generation
    #ai_keywords = generator.KeywordsGeneration(topic = "Payments FinTech startups")

    # 1. Content Generation
    generated_post = generator.generate_blog_post(keyword)

    # for keyword in ai_keywords:
    #     generated_post = generator.generate_blog_post(keyword)

    # 2. SEO Optimization
    seo = SEOOptimizer(keyword="FinTech", recommended_keyword_density=[0.01, 0.02])
    optimized_post = seo.optimize_blog(generated_post)

    print("Final Blog Post:\n", optimized_post)
