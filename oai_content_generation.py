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

    def GenerateBlogPost(self, keyword: str, max_tokens = 700, temperature = 0.7) -> str:
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