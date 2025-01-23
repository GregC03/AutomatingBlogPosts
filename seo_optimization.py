import re
import textstat
import difflib
from textblob import TextBlob

class SEOAnalyzer:
    def __init__(self):
        pass

    def check_keywords(self, content, target_keywords):
        results = {}
        for keyword in target_keywords:
            keyword_count = len(re.findall(r'\b' + re.escape(keyword) + r'\b', content, flags=re.IGNORECASE))
            if keyword_count == 0:
                results[keyword] = "Keyword not found"
            elif keyword_count < 2:
                results[keyword] = f"Keyword used {keyword_count} time"
            else:
                results[keyword] = f"Keyword used {keyword_count} times"
        report = ""
        for keyword, outcome in results.items():
            task = "Add more instances of this keyword for better optimization." if "not found" in outcome else "Ensure keyword density is optimal."
            report += f"Keyword Usage Check - {keyword}: {outcome}. Task: {task}\n"
        return report
    
    def check_content_length(self, content, min_length=300):
        word_count = len(content.split())
        if word_count < min_length:
            return f"Content Length Check: Content is too short. {word_count} words. Minimum is {min_length} words. Task: Add more detailed information to meet the minimum word count.\n"
        return "Content Length Check: Content length is optimal. No changes needed.\n"
    
    def check_title_length(self, title):
        if len(title) < 50 or len(title) > 60:
            return f"Title Length Check: Title length is {len(title)} characters. Should be between 50-60 characters. Task: Adjust the title length to be between 50-60 characters.\n"
        return "Title Length Check: Title length is optimal. No changes needed.\n"
    
    def check_meta_description(self, meta_description):
        if len(meta_description) < 140 or len(meta_description) > 160:
            return f"Meta Description Check: Meta description length is {len(meta_description)} characters. Should be between 140-160 characters. Task: Revise the meta description to be within 140-160 characters.\n"
        return "Meta Description Check: Meta description length is optimal. No changes needed.\n"
    
    def check_readability(self, text):
        score = textstat.flesch_kincaid_grade(text)
        if score > 8:
            return f"Readability Check: Flesch-Kincaid readability score is {score}. Task: Simplify the language to make the content easier to read.\n"
        return f"Readability Check: Flesch-Kincaid readability score is {score}. No changes needed.\n"
    
    def check_sentence_length(self, content, max_length=25):
        sentences = content.split('.')
        sentence_lengths = [len(sentence.split()) for sentence in sentences if sentence]
        long_sentences = [length for length in sentence_lengths if length > max_length]
        if long_sentences:
            return f"Sentence Length Check: {len(long_sentences)} sentences exceed {max_length} words. Task: Break up long sentences into shorter ones for better readability.\n"
        return "Sentence Length Check: Sentence lengths are optimal. No changes needed.\n"
    
    #def check_content_duplication(self, content, existing_content):
    #    similarity_ratio = difflib.SequenceMatcher(None, content, existing_content).ratio()
    #    if similarity_ratio > 0.8:
    #        return f"Content Duplication Check: Content is too similar to existing content (similarity ratio: {similarity_ratio}). Task: Revise the content to make it more original.\n"
    #    return "Content Duplication Check: Content is unique. No changes needed.\n"
    
    def check_content_duplication(self, content: str, existing_contents: list[str]) -> str:
        max_similarity = 0
        for existing_content in existing_contents:
            similarity_ratio = difflib.SequenceMatcher(None, content, existing_content).ratio()
            max_similarity = max(max_similarity, similarity_ratio)
        
        if max_similarity > 0.8:
            return f"Content Duplication Check: Content is too similar to existing content (similarity ratio: {max_similarity}). Task: Revise the content to make it more original.\n"
        return "Content Duplication Check: Content is unique. No changes needed.\n"

    def check_keyword_density(self, content, keyword):
        keyword_count = content.lower().split().count(keyword.lower())
        total_words = len(content.split())
        keyword_density = (keyword_count / total_words) * 100
        if keyword_density > 2:
            return f"Keyword Density Check: Keyword density for '{keyword}' is {keyword_density:.2f}%. Task: Reduce keyword usage to avoid keyword stuffing.\n"
        return f"Keyword Density Check: Keyword density for '{keyword}' is {keyword_density:.2f}%. No changes needed.\n"
    
    def check_paragraphs_and_subheadings(self, content):
        paragraphs = content.split('\n\n')
        subheadings = [line for line in content.split('\n') if line.strip().startswith('#')]
        if len(paragraphs) < 3:
            return "Paragraph Structure Check: Less than 3 paragraphs found. Task: Break content into more paragraphs.\n"
        if len(subheadings) < 2:
            return "Subheading Check: Less than 2 subheadings found. Task: Add more subheadings to break the content.\n"
        return "Paragraph and Subheading Structure Check: Proper structure. No changes needed.\n"
    
    def check_sentiment(self, content):
        blob = TextBlob(content)
        sentiment = blob.sentiment
        if sentiment.polarity < 0:
            return f"Sentiment Check: Content has a negative tone. Sentiment score: {sentiment.polarity}. Task: Revise the content to ensure a more positive and professional tone.\n"
        return f"Sentiment Check: Content has a positive tone. Sentiment score: {sentiment.polarity}. No changes needed.\n"
    
    def check_heading_structure(self, content):
        headings = [line for line in content.split('\n') if line.strip().startswith('#')]
        if not headings:
            return "Heading Structure Check: No headings found. Task: Add headings to break up the content into sections.\n"
        return "Heading Structure Check: Proper heading structure. No changes needed.\n"
    
    def generate_report(self, content, target_keywords, title, meta_description, existing_contents):
        final_report = ""
        final_report += self.check_keywords(content, target_keywords)
        final_report += self.check_content_length(content)
        final_report += self.check_title_length(title)
        final_report += self.check_meta_description(meta_description)
        final_report += self.check_readability(content)
        final_report += self.check_sentence_length(content)
        final_report += self.check_content_duplication(content, existing_contents)
        final_report += self.check_keyword_density(content, target_keywords[0])
        final_report += self.check_paragraphs_and_subheadings(content)
        final_report += self.check_sentiment(content)
        return final_report
    
'''def check_keywords(content, target_keywords):
    results = {}
    for keyword in target_keywords:
        keyword_count = len(re.findall(r'\b' + re.escape(keyword) + r'\b', content, flags=re.IGNORECASE))
        if keyword_count == 0:
            results[keyword] = "Keyword not found"
        elif keyword_count < 2:
            results[keyword] = f"Keyword used {keyword_count} time"
        else:
            results[keyword] = f"Keyword used {keyword_count} times"
    report = ""
    for keyword, outcome in results.items():
        task = "Add more instances of this keyword for better optimization." if "not found" in outcome else "Ensure keyword density is optimal."
        report += f"Keyword Usage Check - {keyword}: {outcome}. Task: {task}\n"
    return report

content = "This is the content of the blog post with some words like FinTech and blockchain."
target_keywords = ['FinTech', 'blockchain', 'investment']
print(check_keywords(content, target_keywords))

def check_content_length(content, min_length=300):
    word_count = len(content.split())
    if word_count < min_length:
        return f"Content Length Check: Content is too short. {word_count} words. Minimum is {min_length} words. Task: Add more detailed information to meet the minimum word count.\n"
    return "Content Length Check: Content length is optimal. No changes needed.\n"

content = "This is the content of the blog post."
print(check_content_length(content))

def check_title_length(title):
    if len(title) < 50 or len(title) > 60:
        return f"Title Length Check: Title length is {len(title)} characters. Should be between 50-60 characters. Task: Adjust the title length to be between 50-60 characters.\n"
    return "Title Length Check: Title length is optimal. No changes needed.\n"

title = "How Blockchain is Revolutionizing the FinTech Industry"
print(check_title_length(title))

def check_meta_description(meta_description):
    if len(meta_description) < 140 or len(meta_description) > 160:
        return f"Meta Description Check: Meta description length is {len(meta_description)} characters. Should be between 140-160 characters. Task: Revise the meta description to be within 140-160 characters.\n"
    return "Meta Description Check: Meta description length is optimal. No changes needed.\n"

meta_description = "This is an example of a good meta description for a FinTech blog post."
print(check_meta_description(meta_description))



def check_readability(text):
    score = textstat.flesch_kincaid_grade(text)
    if score > 8:  # If the score is too high, the content is hard to read
        return f"Readability Check: Flesch-Kincaid readability score is {score}. Task: Simplify the language to make the content easier to read.\n"
    return f"Readability Check: Flesch-Kincaid readability score is {score}. No changes needed.\n"

text = "Your blog post text goes here."
print(check_readability(text))

def check_sentence_length(content, max_length=25):
    sentences = content.split('.')
    sentence_lengths = [len(sentence.split()) for sentence in sentences if sentence]
    long_sentences = [length for length in sentence_lengths if length > max_length]
    if long_sentences:
        return f"Sentence Length Check: {len(long_sentences)} sentences exceed {max_length} words. Task: Break up long sentences into shorter ones for better readability.\n"
    return "Sentence Length Check: Sentence lengths are optimal. No changes needed.\n"

content = "This is a sentence. This one is a bit longer. It might go over the threshold depending on how long it is."
print(check_sentence_length(content))



def check_content_duplication(content, existing_content):
    similarity_ratio = difflib.SequenceMatcher(None, content, existing_content).ratio()
    if similarity_ratio > 0.8:
        return f"Content Duplication Check: Content is too similar to existing content (similarity ratio: {similarity_ratio}). Task: Revise the content to make it more original.\n"
    return "Content Duplication Check: Content is unique. No changes needed.\n"

content = "This is a blog post content."
existing_content = "This is some existing blog post content."
print(check_content_duplication(content, existing_content))

def check_keyword_density(content, keyword):
    keyword_count = content.lower().split().count(keyword.lower())
    total_words = len(content.split())
    keyword_density = (keyword_count / total_words) * 100
    if keyword_density > 2:  # If keyword density is higher than 2%, it's too much
        return f"Keyword Density Check: Keyword density for '{keyword}' is {keyword_density:.2f}%. Task: Reduce keyword usage to avoid keyword stuffing.\n"
    return f"Keyword Density Check: Keyword density for '{keyword}' is {keyword_density:.2f}%. No changes needed.\n"

content = "FinTech is an innovative field. The future of FinTech is exciting."
keyword = "FinTech"
print(check_keyword_density(content, keyword))

def check_paragraphs_and_subheadings(content):
    paragraphs = content.split('\n\n')
    subheadings = [line for line in content.split('\n') if line.strip().startswith('#')]
    if len(paragraphs) < 3:
        return f"Paragraph Structure Check: Less than 3 paragraphs found. Task: Break content into more paragraphs.\n"
    if len(subheadings) < 2:
        return f"Subheading Check: Less than 2 subheadings found. Task: Add more subheadings to break the content.\n"
    return "Paragraph and Subheading Structure Check: Proper structure. No changes needed.\n"

content = """# Introduction
This is the introduction paragraph.

# Subheading 1
This is the first subheading paragraph.

# Subheading 2
This is another paragraph under subheading 2."""
print(check_paragraphs_and_subheadings(content))



def check_sentiment(content):
    blob = TextBlob(content)
    sentiment = blob.sentiment
    if sentiment.polarity < 0:
        return f"Sentiment Check: Content has a negative tone. Sentiment score: {sentiment.polarity}. Task: Revise the content to ensure a more positive and professional tone.\n"
    return f"Sentiment Check: Content has a positive tone. Sentiment score: {sentiment.polarity}. No changes needed.\n"

content = "FinTech is revolutionizing the financial industry. It's an exciting time for investors."
print(check_sentiment(content))


final_report = ""

# Add the results of all checks
final_report += check_keywords(content, target_keywords)
final_report += check_content_length(content)
final_report += check_title_length(title)
final_report += check_meta_description(meta_description)
final_report += check_readability(content)
final_report += check_sentence_length(content)
final_report += check_content_duplication(content, existing_content)
final_report += check_keyword_density(content, keyword)
final_report += check_paragraphs_and_subheadings(content)
final_report += check_sentiment(content)

# Print the final report
print(final_report)
'''