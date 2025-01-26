''' Module based on OpenAI API Calls with classes and methods for:
    1) generating content such as keywords, blog posts, titles, and meta descriptions;
    2) a class that puts togerher the conent generation from the previous class and outputs the final content to be then optimized for SEO;
    3) fixing the latter content for SEO optimization, using AI models  and the instructions provided,
       usually obtained from the "SEO_optimization.py" module.'''

# Importing from external libraries
import os
import openai
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor, as_completed

def _LoadOaiKey():
    load_dotenv()
    return os.getenv("OPENAI_API_KEY")

def _SetOaiKey():
    openai.api_key = _LoadOaiKey()

class OaiContentGenerator:
    def __init__(self, model_name = "gpt-4o-mini"):
        self.model_name = model_name
        _SetOaiKey()

    def GenerateKeywords(self, topic: str = "fintech startups", max_tokens = 50, temperature = 0.7) -> str:
        '''Generates a list of keywords based on the topic'''

        system = (
            f"You are a senior SEO strategist specializing in {topic} content marketing. "
            "Your expertise lies in identifying high-impact keywords that drive organic traffic to your company's blog. "
            f"You understand both technical SEO principles and industry trends related to the {topic}. "
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
            f"Then, group the keywords into sublists of 1 to 3 keywords based on their relevance, search intent and concept similarity."
            f"For each sublist of keywords select the most relevant keyword that best represents the group."
            f"Finally provide the outcome as a list of the sublists with the most relevant keyword for each sublist at the beginning of each sublist."
            f"Output example: 'keyword11, keyword12, keyword13, ..., keyword1N; keyword21, keyword22, keyword23, ..., keyword2N; ...; keywordM1, keywordM2, keywordM3, ..., keywordMN'"
            f"Make sure that the response only contains the sublists separated by semicolons and the keywords separated by commas"
        )


        response = openai.ChatCompletion.create(
            model=self.model_name,
            messages=[{"role": "system", "content": system},
                      {"role": "user", "content": prompt}
                      ],
            max_completion_tokens=max_tokens, #max_completion_tokens is better
            temperature=temperature
        )

        # Extract the message from the API response
        generated_keywords = response["choices"][0]["message"]["content"]
        try:
            outputs = generated_keywords.split(";")
            for i,output in enumerate(outputs):
                outputs[i] = output.split(",")
            return outputs
        except ValueError:
            return "The response from the AI was not in the expected format. Please try again."
        
    def GenerateKeywordsFromSearchResults(self, search_results: list, topic: str, max_tokens = 50, temperature = 0.6) -> str:
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
            f"Ensure all keywords align with SEO best practices and FinTech industry standards. "
            f"Then, group the keywords into sublists of 1 to 3 keywords based on their relevance, search intent and concept similarity."
            f"For each sublist of keywords select the most relevant keyword that best represents the group."
            f"Finally provide the outcome as a list of the sublists with the most relevant keyword for each sublist at the beginning of each sublist."
            f"Output example: 'keyword11, keyword12, keyword13, ..., keyword1N; keyword21, keyword22, keyword23, ..., keyword2N; ...; keywordM1, keywordM2, keywordM3, ..., keywordMN'"
            f"Make sure that the response only contains the sublists separated by semicolons and the keywords separated by commas"
        )

        response = openai.ChatCompletion.create(
            model=self.model_name,
            messages=[{"role": "system", "content": system},
                      {"role": "user", "content": prompt}
                      ],
            max_completion_tokens=max_tokens,
            temperature=temperature
        )

        # Extract the message from the API response
        generated_keywords = response["choices"][0]["message"]["content"]
        try:
            outputs = generated_keywords.split(";")
            for i,output in enumerate(outputs):
                outputs[i] = output.split(",")
            return outputs
        except ValueError:
            return "The response from the AI was not in the expected format. Please try again."

    def GenerateBlogPost(self, topic, keywords: list[str], max_tokens = 2000, temperature = 0.5) -> str: # set token to 2000
        '''Generates a blog post based on the keyword'''

        system = (
            "You are an expert SEO copywriter specializing in FinTech content. "
            "You excel at creating engaging, well-researched articles that rank highly in search engines. "
            "Your writing style combines technical accuracy with clear explanations for both beginners and experts. "
            "You follow modern SEO best practices, including proper heading hierarchy, optimal keyword placement, "
            "and reader-friendly formatting with short paragraphs and bullet points."
            f"Your task is to write a comprehensive blog post for a FinTech audience about the keywords in this list: '{keywords}'."
        )

        prompt = (
            f"Write a comprehensive blog post for a FinTech audience about the keywords in this list: '{keywords}'. The post should include:\n"
            f"1. An engaging introduction that hooks the reader\n"
            f"2. 3-5 main sections with H2 headings\n"
            f"3. Relevant subsections with H3 headings where appropriate\n"
            f"4. A clear conclusion summarizing key points\n"
            f"5. A practical bullet list of actionable takeaways\n"
            f"6. A strong call-to-action\n\n"
            f"Maintain natural keywords density (1-2%), use transition words for flow, "
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
            "You follow modern SEO best practices, including proper heading hierarchy (H1, H2, H3), optimal keyword placement, "
            "and reader-friendly formatting with short paragraphs and bullet points."
        )

        prompt = (
            f"Generate a SEO-optimized, attention-grabbing title with H1 heading for the following blog post with the main keyword '{keyword}':\n\n"
            f"{blog_text}"
            f"The title should be concise, engaging, and include the main keyword '{keyword}' to attract readers and improve search engine visibility."
            f"Ensure the title is between 50-60 characters for optimal display in search results."
            f"Remember to maintain a professional yet engaging tone throughout the title."
            f"Ensure that it is formatted correctly with respect to proper heading hierarchy (H1). It must not contain any indications such as 'Title:' or similar."
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
            "You follow modern SEO best practices, including proper heading hierarchy (H1, H2, H3), optimal keyword placement, "
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


class ContentGeneration:
    def __init__(self):
        pass
    
    def Posts_Titles_Metadescriptions_Generator(self, generation_model: str, final_keywords: list[list[str]]) -> tuple:

        generator = OaiContentGenerator(model_name=generation_model)
        generated_posts = []
        generated_titles = []
        generated_metadescriptions = []
        
        def generate_content(keywords):
            post = generator.GenerateBlogPost(topic=keywords, keywords=keywords)
            title = generator.GeneratePostTitle(blog_text=post, keyword=keywords)
            metadescription = generator.GeneratePostMetaDescription(blog_text=post, blog_title=title, keyword=keywords)
            return post, title, metadescription
        
        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(generate_content, keywords) for keywords in final_keywords]
            for future in as_completed(futures):
                post, title, metadescription = future.result()
                generated_posts.append(post)
                generated_titles.append(title)
                generated_metadescriptions.append(metadescription)
        
        return generated_posts, generated_titles, generated_metadescriptions


class OaiSeoSpecialist:
    def __init__(self, model_name = "gpt-4o-mini"):
        self.model_name = model_name
        _SetOaiKey()

    def FixBlogPost(self, blog_text: str, instructions: str, max_tokens = 2400, temperature = 0.5) -> str: # set tokens to 2000
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
    
    def FixBlogTitle(self, blog_title: str, instructions: str, max_tokens = 80, temperature = 0.5) -> str:
        system = (
            "You are an expert SEO copywriter and editor specialized in FinTech content. "
            "Your role is to enhance blog posts following specific editorial guidelines while maintaining SEO best practices. "
            "You excel at implementing precise content modifications while preserving the original message and improving readability. "
            "Focus on maintaining consistent tone, proper keyword density (1-2%), and clear structure with appropriate headings."
        )

        prompt = (
            f"Revise the following blog title according to these specific instructions:\n\n"
            f"INSTRUCTIONS:\n{instructions}\n\n"
            f"ORIGINAL TITLE:\n{blog_title}\n\n"
            f"Please ensure that the revised version:\n"
            f"1. Follows all provided instructions\n"
            f"2. Maintains the original message and tone\n"
            f"3. Enhances readability and SEO optimization\n"
            f"4. Does not include the instructions in the revised content."
            f"5. Does not include things such as 'Revised Title:' at the beginning of the revised content."
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
        fixed_title = response["choices"][0]["message"]["content"]
        return fixed_title
    
    def FixMetaDescription(self, meta_description: str, instructions: str, max_tokens = 220, temperature = 0.5) -> str:

        system = (
            "You are an expert SEO copywriter and editor specialized in FinTech content. "
            "Your role is to enhance blog posts following specific editorial guidelines while maintaining SEO best practices. "
            "You excel at implementing precise content modifications while preserving the original message and improving readability. "
            "Focus on maintaining consistent tone, proper keyword density (1-2%), and clear structure with appropriate headings."
        )

        prompt = (
            f"Revise the following meta description according to these specific instructions:\n\n"
            f"INSTRUCTIONS:\n{instructions}\n\n"
            f"ORIGINAL META DESCRIPTION:\n{meta_description}\n\n"
            f"Please ensure that the revised version:\n"
            f"1. Follows all provided instructions\n"
            f"2. Maintains the original message and tone\n"
            f"3. Enhances readability and SEO optimization\n"
            f"4. Does not include the instructions in the revised content."
            f"5. Does not include things such as 'Revised Meta Description:' at the beginning of the revised content."
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
        fixed_description = response["choices"][0]["message"]["content"]
        return fixed_description
    
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
    
