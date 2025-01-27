'''Module for managing internal linking within the website and the blog posts'''

import numpy as np
import pandas as pd
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class InternalLinking:
    def __init__(self):
        pass

    def generate_internal_links(self, posts: list[str], titles: list[str], metadescriptions: list[str] , keywords: list[list[str]], previous_posts_path: str = "./data/automated_blog_posts.csv") -> list[list[str]]:
        '''Generate internal links for SEO optimization'''
        # Import previous blog posts, titles, meta descriptions, and keywords
        
        if os.path.exists(previous_posts_path):
            df = pd.read_csv(previous_posts_path, sep=';')
            previous_posts = df['blog_post'].tolist()
            previous_titles = df['title'].tolist()
            previous_metadescriptions = df['meta_description'].tolist()
            previous_keywords = df['keyword'].tolist()
        else:
            print("No previous blog posts found.")
            return [[] for _ in range(len(posts))]
        
        
        # check conceptual and semantic similarity between the blog posts and old posts
        similarity_matrix = np.zeros((len(posts), len(previous_posts)))
        for i, post in enumerate(posts):
            # Compute similarity between the current post and the previous posts
            for j, prev_post in enumerate(previous_posts):
                similarity = self.compute_similarity(post, prev_post, titles[i], previous_titles[j], metadescriptions[i], previous_metadescriptions[j], keywords[i], previous_keywords[j])
                if similarity > 0.5:
                    similarity_matrix[i][j] = 1


        # Generate internal links based on the similarity matrix
        internal_links = []
        for i, post in enumerate(posts):
            internal_links.append([])

            # Add internal links to the current post
            for j, prev_post in enumerate(previous_posts):
                if similarity_matrix[i][j] == 1:
                    # generate internal link
                    internal_link = f'<a href="/posts/{previous_titles[j].replace(" ", "-").lower()}">{previous_titles[j]}</a>'

                    # Add the internal link to the current post
                    internal_links[i].append(internal_link)

        return internal_links




    def compute_similarity(self, post1: str, post2: str, title1: str, title2: str, metadescription1: str, metadescription2: str , keywords1: list[str], keywords2: list[str]) -> float:
        '''Compute the similarity between two blog posts using NLP techniques'''
        posts = [post1, post2]
        titles = [title1, title2]
        metadescriptions = [metadescription1, metadescription2]
        keywords = [keywords1, keywords2]

        # Combine the posts, titles, and keywords
        texts = []
        for i in range(2):
            texts.append(titles[i] + " " + metadescriptions[i]+ " " + posts[i] + " " + " ".join(keywords[i]))

        vectorizer = TfidfVectorizer().fit_transform(texts)
        vectors = vectorizer.toarray()
        cosine_sim = cosine_similarity(vectors)
        return cosine_sim[0][1]
        
        
