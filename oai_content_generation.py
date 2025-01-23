import os
import openai
from dotenv import load_dotenv

def _LoadOaiKey():
    load_dotenv()
    return os.getenv("OPENAI_API_KEY")

def _SetOaiKey():
    openai.api_key = _LoadOaiKey()

class OaiContentGenerator:
    def __init__(self, model_name = "gpt-3.5-turbo"):
        self.model_name = model_name
        _SetOaiKey()

    def GenerateKeywords(self, topic: str = "fintech startups", max_tokens = 50, temperature = 0.7) -> str:
        '''Generates a list of keywords based on the topic'''

        system = (
            "You are a senior SEO strategist specializing in FinTech content marketing. "
            "Your expertise lies in identifying high-impact keywords that drive organic traffic. "
            "You understand both technical SEO principles and FinTech industry trends. "
            "Your goal is to create a comprehensive keyword strategy that balances search volume, "
            "competition level, and user intent."
        )

        prompt = (
            f"Generate a strategic keyword list for '{topic}' targeting the FinTech sector. "
            f"Include:\n"
            f"1. Primary short-tail keywords with high search volume\n"
            f"2. Long-tail keywords that indicate purchase intent\n"
            f"3. Industry-specific technical terms\n"
            f"4. Question-based keywords reflecting user queries\n"
            f"Ensure all keywords align with SEO best practices and FinTech industry standards. "
            f"Format the response as comma-separated values only: 'keyword1, keyword2, keyword3, ..., keywordN'"
        )

        response = openai.ChatCompletion.create(
            model=self.model_name,
            messages=[{"role": "system", "content": system},
                      {"role": "user", "content": prompt},
                      {"role": "user", "content": "Make sure that the response only contains the Keywords separated by commas, like this: 'keyword1, keyword2, keyword3, ..., keywordN'."}],
            max_completion_tokens=max_tokens, #max_completion_tokens is better
            temperature=temperature
        )

        # Extract the message from the API response
        generated_keywords = response["choices"][0]["message"]["content"]
        try:
            output = generated_keywords.split(",")
            return output
        except ValueError:
            return "The response from the AI was not in the expected format. Please try again."
        
    def GenerateKeywordsFromSearchResults(self, search_results: list, topic: str, max_tokens = 50, temperature = 0.5) -> str:
        '''Generates a list of keywords based on the provided search results'''

        system = (
            "You are a senior SEO and keyword strategist specializing in FinTech marketing. "
            "Your expertise lies in analyzing search data and identifying high-value keyword opportunities. "
            "Your task is to extract meaningful keyword patterns from search result data and combine them "
            f"with industry knowledge to create targeted keyword lists for '{topic}'. "
            "Focus on keywords that balance search volume, competition, and user intent."
        )

        prompt = (
            f"Based on these search result frequency data: {search_results}\n"
            f"Generate a strategic keyword list for '{topic}' that:\n"
            "1. Leverages the most frequent terms from search results\n"
            "2. Includes both short-tail (1-2 words) and long-tail (3+ words) keywords\n"
            "3. Focuses on terms with clear commercial or informational intent\n"
            "4. Incorporates FinTech industry terminology\n\n"
            "Format output as comma-separated values ONLY: 'keyword1, keyword2, keyword3'"
        )

        response = openai.ChatCompletion.create(
            model=self.model_name,
            messages=[{"role": "system", "content": system},
                      {"role": "user", "content": prompt},
                      {"role": "user", "content": "Make sure that the response only contains the Keywords separated by commas, like this: 'keyword1, keyword2, keyword3, ..., keywordN'."}],
            max_completion_tokens=max_tokens,
            temperature=temperature
        )

        # Extract the message from the API response
        generated_keywords = response["choices"][0]["message"]["content"]
        try:
            output = generated_keywords.split(",")
            return output
        except ValueError:
            return "The response from the AI was not in the expected format. Please try again."

    def GenerateBlogPost(self, keyword: str, max_tokens = 2000, temperature = 0.5) -> str: # set token to 2000
        '''Generates a blog post based on the keyword'''

        system = (
            "You are an expert SEO copywriter specializing in FinTech content. "
            "You excel at creating engaging, well-researched articles that rank highly in search engines. "
            "Your writing style combines technical accuracy with clear explanations for both beginners and experts. "
            "You follow modern SEO best practices, including proper heading hierarchy, optimal keyword placement, "
            "and reader-friendly formatting with short paragraphs and bullet points."
        )

        prompt = (
            f"Write a comprehensive blog post about '{keyword}' for a FinTech audience. The post should include:\n"
            f"1. An engaging introduction that hooks the reader\n"
            f"2. 3-5 main sections with H2 headings\n"
            f"3. Relevant subsections with H3 headings where appropriate\n"
            f"4. A clear conclusion summarizing key points\n"
            f"5. A practical bullet list of actionable takeaways\n"
            f"6. A strong call-to-action\n\n"
            f"Maintain natural keyword density (1-2%), use transition words for flow, "
            f"and keep paragraphs under 3-4 sentences for readability. "
            f"Balance professional expertise with an approachable, conversational tone."
            f"The post must not include the title nor the meta description,."
        )

        response = openai.ChatCompletion.create(
            model=self.model_name,
            messages=[{"role": "system", "content": system},
                      {"role": "user", "content": prompt}],
            max_completion_tokens=max_tokens,
            temperature=temperature
        )

        # Extract the message from the API response
        generated_text = response["choices"][0]["message"]["content"]
        return generated_text
    
    def GeneratePostTitle(self, blog_text: str, keyword: str, max_tokens = 80, temperature = 0.5) -> str:
        '''Generates a title for a blog post based on the content'''

        system = (
            "You are an expert SEO copywriter specializing in FinTech content. "
            "You excel at creating engaging, well-researched articles that rank highly in search engines. "
            "Your writing style combines technical accuracy with clear explanations for both beginners and experts. "
            "You follow modern SEO best practices, including proper heading hierarchy, optimal keyword placement, "
            "and reader-friendly formatting with short paragraphs and bullet points."
        )

        prompt = (
            f"Generate a SEO-optimized, attention-grabbing title with H1 heading for the following blog post with the main keyword '{keyword}':\n\n"
            f"{blog_text}"
            f"The title should be concise, engaging, and include the main keyword '{keyword}' to attract readers and improve search engine visibility."
            f"Ensure the title is between 50-60 characters for optimal display in search results."
            f"Remember to maintain a professional yet engaging tone throughout the title."
            f"Ensure that it is formatted correctly with respect to proper heading hierarchy (H1). It must be introduced by 'Title:' and end with a period."
        )

        response = openai.ChatCompletion.create(
            model=self.model_name,
            messages=[{"role": "system", "content": system},
                      {"role": "user", "content": prompt}],
            max_completion_tokens=max_tokens,
            temperature=temperature
        )

        # Extract the message from the API response
        generated_title = response["choices"][0]["message"]["content"]
        return generated_title

    def GeneratePostMetaDescription(self, blog_text: str, blog_title: str, keyword: str, max_tokens = 220, temperature = 0.5) -> str:
        '''Generates a meta description for a blog post based on the content'''

        system = (
            "You are an expert SEO copywriter specializing in FinTech content. "
            "You excel at creating engaging, well-researched articles that rank highly in search engines. "
            "Your writing style combines technical accuracy with clear explanations for both beginners and experts. "
            "You follow modern SEO best practices, including proper heading hierarchy, optimal keyword placement, "
            "and reader-friendly formatting with short paragraphs and bullet points."
        )

        prompt = (
            f"Generate a SEO-optimized, compelling meta description (150-160 characters) for the following blog post with title '{blog_title}' and main keyword '{keyword}':\n\n"
            f"{blog_text}"
            f"The meta description should be concise, engaging, and include the main keyword '{keyword}' to attract readers and improve search engine visibility."
            f"Ensure the meta description is between 150-160 characters for optimal display in search results."
            f"Remember to maintain a professional yet engaging tone throughout the meta description."
            f"Ensure that it is formatted correctly with respect to proper heading hierarchy. It must be introduced by 'Meta Description:' and end with a period."

        )

        response = openai.ChatCompletion.create(
            model=self.model_name,
            messages=[{"role": "system", "content": system},
                      {"role": "user", "content": prompt}],
            max_completion_tokens=max_tokens,
            temperature=temperature
        )
        
        # Extract the message from the API response
        generated_description = response["choices"][0]["message"]["content"]
        return generated_description




class OaiSeoSpecialist:
    def __init__(self, model_name = "gpt-3.5-turbo"):
        self.model_name = model_name
        _SetOaiKey()

    def FixBlogPost(self, blog_text: str, instructions: str, max_tokens = 2400, temperature = 0.4) -> str: # set tokens to 2000
        '''Fixes a blog post based on the given instructions'''
    
        system = (
            "You are an expert SEO copywriter and editor specialized in FinTech content. "
            "Your role is to enhance blog posts following specific editorial guidelines while maintaining SEO best practices. "
            "You excel at implementing precise content modifications while preserving the original message and improving readability. "
            "Focus on maintaining consistent tone, proper keyword density (1-2%), and clear structure with appropriate headings."
        )

        prompt = (
            f"Revise the following blog post according to these specific instructions:\n\n"
            f"INSTRUCTIONS:\n{instructions}\n\n"
            f"ORIGINAL POST:\n{blog_text}\n\n"
            f"Please ensure that the revised version:\n"
            f"1. Follows all provided instructions\n"
            f"2. Maintains the original message and tone\n"
            f"3. Enhances readability and SEO optimization\n"
            f"4. Includes proper heading hierarchy (H1, H2, and H3) and keyword placement\n"
            f"2. Does not include the instructions in the revised content."
            f"3. Does not include things such as 'Revised Content:' or 'Revised Post:' at the beginning of the revised content."
            f"Again, you must ensure that you follow the instructions provided at the beginning and revise the content accordingly."
        )

        response = openai.ChatCompletion.create(
            model=self.model_name,
            messages=[{"role": "system", "content": system},
                      {"role": "user", "content": prompt}],
            max_completion_tokens=max_tokens,
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
            "Ensure the content follows best SEO practices, uses appropriate headings (H2, H3) and short paragraphs, and enhances keyword optimization."
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
            max_completion_tokens=max_tokens,
            temperature=temperature
        )

        improved_text = response["choices"][0]["message"]["content"]
        return improved_text