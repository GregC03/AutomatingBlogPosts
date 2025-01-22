from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

class ContentGenerator:
    def __init__(self, model_name = 'EleutherAI/gpt-neo-1.3B'):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(model_name)
        # If you have GPU:
        self.model = self.model.cuda()

    def GenerateBlogContent(self, keyword, max_length = 300, temperature = 0.7):
        '''Generate blog content based on the keyword'''

        prompt = f"Write a blog post about {keyword}."