# seo_optimizer.py

import re
import math
from collections import Counter
import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')

from 

class SEOOptimizer:
    def __init__(self, keyword: str, recommended_keyword_density=[0.01,0.02]):
        """
        Initialize with a primary keyword and a recommended density range
        (e.g. 1%-2%).
        """
        self.keyword = keyword.lower()
        self.recommended_keyword_density_min = recommended_keyword_density[0]
        self.recommended_keyword_density_max = recommended_keyword_density[1]
        self.stop_words = set(stopwords.words('english'))

    def compute_word_count(self, text: str) -> int:
        """
        Compute total word count in the text.
        """
        words = re.findall(r"\w+", text.lower())
        return len(words)

    def compute_keyword_density(self, text: str) -> float:
        """
        Compute the density of the primary keyword in the text.
        """
        words = re.findall(r"\w+", text.lower())
        total_words = len(words)
        if total_words == 0:
            return 0
        count_keyword = sum(1 for w in words if w == self.keyword)
        return count_keyword / total_words

    def optimize_blog(self, blog_text: str) -> str:
        """
        Simple optimizer that tries to adjust keyword density
        by inserting the primary keyword if below recommended density.
        """
        current_density = self.compute_keyword_density(blog_text)
        total_words = self.compute_word_count(blog_text)
        required_count_min = math.floor(total_words * self.recommended_keyword_density_min)
        required_count_max = math.floor(total_words * self.recommended_keyword_density_max)

        # Check if the keyword is already present


        # Insert the keyword if density is too low
        if (current_density < self.recommended_keyword_density_min) and (required_count_min> 0):
            shortfall = required_count_min - math.floor(total_words * current_density)
            # Insert the keyword randomly
            for _ in range(shortfall):
                blog_text += f" {self.keyword}"

        # Remove extra keywords if density is too high
        elif (current_density > self.recommended_keyword_density_max) and (required_count_max > 0):
            excess = math.floor(total_words * current_density) - required_count_max
            # Remove the keyword randomly
            words = re.findall(r"\w+", blog_text.lower())
            keyword_indices = [i for i, w in enumerate(words) if w == self.keyword]
            for _ in range(excess):
                if keyword_indices:
                    index = keyword_indices.pop()
                    words[index] = ""
            blog_text = " ".join(words)

        return blog_text

if __name__ == "__main__":
    # Example usage
    text = """Financial planning is crucial for young professionals. 
              It sets the stage for a secure future and prudent investments."""
    seo = SEOOptimizer(keyword="financial", recommended_keyword_density=0.02)
    optimized_text = seo.optimize_blog(text)
    print("Optimized Blog Content:\n", optimized_text)
