# main.py

from oai_content_generation import OaiContentGenerator
from seo_optimizer import SEOOptimizer

if __name__ == "__main__":
    keyword = "FinTech innovation in 2025"

    # 1. Content Generation
    generator = OaiContentGenerator(model_name="EleutherAI/gpt-neo-1.3B", max_length=500)
    generated_post = generator.generate_blog_post(keyword)

    # 2. SEO Optimization
    seo = SEOOptimizer(primary_keyword="FinTech", recommended_keyword_density=0.015)
    optimized_post = seo.optimize_blog(generated_post)

    print("Final Blog Post:\n", optimized_post)
