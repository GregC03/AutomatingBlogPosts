import os
import openai
from dotenv import load_dotenv

def LoadOaiKey():
    load_dotenv()
    return os.getenv("OPENAI_API_KEY")

def SetOaiKey():
    openai.api_key = LoadOaiKey()

class OaiContentGenerator:
    def __init__(self, model_name = "gpt-3.5-turbo"):
        self.model_name = model_name
        SetOaiKey()

    def GenerateKeywords(self, topic: str = "fintech startups", max_tokens = 100, temperature = 0.5) -> str:
        '''Generates a list of keywords based on the topic'''

        system = (
            f"You are a digital marketing specialist for a growing FinTech startup."
            f"You are preparing a list of keywords for the company's website. "
            f"Include a mix of short-tail and long-tail keywords."
        )


        prompt = (
            f"Generate a list of keywords related to '{topic}' for a FinTech audience. "
            f"Include a mix of short-tail and long-tail keywords that are relevant to the company's products and services. "
            f"Ensure the keywords are SEO-friendly and have a professional yet approachable tone."
            f"The response must only contains the Keywords separated by commas, like this: 'keyword1, keyword2, keyword3, ..., keywordN'."
        )

        response = openai.ChatCompletion.create(
            model=self.model_name,
            messages=[{"role": "system", "content": system},
                      {"role": "user", "content": prompt},
                      {"role": "user", "content": "Make sure that the response only contains the Keywords separated by commas, like this: 'keyword1, keyword2, keyword3, ..., keywordN'."}],
            max_tokens=max_tokens,
            temperature=temperature
        )

        # Extract the message from the API response
        generated_keywords = response["choices"][0]["message"]["content"]
        try:
            output = generated_keywords.split(",")
            return output
        except ValueError:
            return "The response from the AI was not in the expected format. Please try again."

    def GenerateBlogPost(self, keyword: str, max_tokens = 700, temperature = 0.5) -> str:
        '''Generates a blog post based on the keyword'''

        system = (
            f"You are a helpful SEO copywriter for a blooming FinTech startup."
            f"You write well-structured, SEO-friendly articles. "
            f"Include headings (H2, H3) and short paragraphs."
        )

        prompt = (
            f"Write a long blog post about '{keyword}' for a FinTech audience to be published in the company's website. "
            F"Structure the article with an Introduction, 3-5 Subheadings, a short Conclusion, and a bulleted list of actionable tips. "
            f"Keep language SEO-friendly with a keyword density of around 1-2%, and a professional yet approachable tone."
        )

        response = openai.ChatCompletion.create(
            model=self.model_name,
            messages=[{"role": "system", "content": system},
                      {"role": "user", "content": prompt}],
            max_tokens=max_tokens,
            temperature=temperature
        )

        # Extract the message from the API response
        generated_text = response["choices"][0]["message"]["content"]
        return generated_text
    
    def FixBlogPost(self, blog_text: str, instructions: str, max_tokens = 700, temperature = 0.5) -> str:
        '''Fixes a blog post based on the given instructions'''
        system = (
            f"You are a helpful SEO copywriter whose responsability is to fix problems in blog posts written by other writers at your company."
            f"You write well-structured, SEO-friendly articles. "
            f"Include headings (H2, H3) and short paragraphs."
        )

        prompt = (
            f"Fix the following blog post by following the instructions below: \n\n"
            f"Instructions: {instructions}\n\n"
            f"Blog Post:\n{blog_text}"
        )

        response = openai.ChatCompletion.create(
            model=self.model_name,
            messages=[{"role": "system", "content": system},
                      {"role": "user", "content": prompt}],
            max_tokens=max_tokens,
            temperature=temperature
        )

        # Extract the message from the API response
        fixed_text = response["choices"][0]["message"]["content"]
        return fixed_text
    
    def ReviewAndImproveSEO(self, blog_text: str, max_tokens=1000, temperature=0.5) -> str:
        '''Reviews a blog post for SEO issues and improves it by fixing such issues.'''

        system = (
            "You are an expert SEO specialist and copywriter. Your job is to analyze blog posts for SEO effectiveness, "
            "detect any issues with keyword density, readability, structure, tone, and engagement, and improve the content accordingly. "
            "Ensure the content follows best SEO practices, uses appropriate headings, and enhances keyword optimization."
            "It is vital for your job that the content is compliant with the latest SEO standards and guidelines."
        )

        prompt = (
            f"Review the following blog post and identify any SEO-related issues such as (but not limited to) keyword optimization, readability, structure, and tone. "
            f"Then, rewrite the content to improve these aspects while maintaining a professional yet friendly style.\n\n"
            f"Blog Post:\n{blog_text}"
        )

        response = openai.ChatCompletion.create(
            model=self.model_name,
            messages=[{"role": "system", "content": system},
                      {"role": "user", "content": prompt}],
            max_tokens=max_tokens,
            temperature=temperature
        )

        improved_text = response["choices"][0]["message"]["content"]
        return improved_text