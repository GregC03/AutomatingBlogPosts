'''Module for integrating with a Content Management System (CMS) like WordPress, Drupal, Joomla, or Wix'''

# Importing from external libraries
import requests
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

class CMSIntegration:
    """Class to integrate with a Content Management System (CMS) like WordPress."""
    def __init__(self):
        self.wordpress_url = os.getenv("WORDPRESS_API_URL")
        self.access_token = os.getenv("WORDPRESS_ACCESS_TOKEN")

    def publish_to_wordpress(self, seo_optimized_posts: list[str], seo_optimized_titles: list[str], seo_optimized_metadescriptions: list[str], final_keywords: list[list[str]], draft: bool=False):
        headers = {
                    "Authorization": f"Bearer {self.access_token}",
                    "Content-Type": "application/json"
                }

        for post, title, metadescription, keywords in zip(seo_optimized_posts, seo_optimized_titles, seo_optimized_metadescriptions, final_keywords):

            if not draft:
                data = {
                    "title": title,
                    "content": post,
                    "status": "publish", 
                    "categories": [1],  # Example category ID
                    "tags": [keywords],
                    "meta": {
                        "description": metadescription
                    }
                }
            else:
                data = {
                    "title": title,
                    "content": post,
                    "status": "draft",
                    "categories": [1],
                    "tags": [keywords],
                    "meta": {
                        "description": metadescription
                    }
                }
            response = requests.post(self.wordpress_url, json=data, headers=headers)
            if response.status_code == 201:
                print(f"Post '{title}' published successfully!")
            else:
                print(f"Error: {response.content}")

    def publsih_to_drupal(self, seo_optimized_posts: list[str], seo_optimized_titles: list[str], seo_optimized_metadescriptions: list[str], final_keywords: list[list[str]], draft: bool=False):
        print("Drupal CMS is not supported yet.")

    def publish_to_joomla(self, seo_optimized_posts: list[str], seo_optimized_titles: list[str], seo_optimized_metadescriptions: list[str], final_keywords: list[list[str]], draft: bool=False):
        print("Joomla CMS is not supported yet.")

    def publish_to_wix(self, seo_optimized_posts: list[str], seo_optimized_titles: list[str], seo_optimized_metadescriptions: list[str], final_keywords: list[list[str]], draft: bool=False):
        print("Wix CMS is not supported yet.")

    def cms_publication(self, seo_optimized_posts, seo_optimized_titles, seo_optimized_metadescriptions, final_keywords, cms_type:str, draft: bool = True):
        if cms_type == "wordpress":
            self.publish_to_wordpress(
                seo_optimized_posts=seo_optimized_posts,
                seo_optimized_titles = seo_optimized_titles,
                seo_optimized_metadescriptions = seo_optimized_metadescriptions,
                final_keywords= final_keywords,
                draft=draft
            )
            if cms_type == "drupal":
                self.publish_to_drupal(
                    seo_optimized_posts=seo_optimized_posts,
                    seo_optimized_titles=seo_optimized_titles,
                    seo_optimized_metadescriptions=seo_optimized_metadescriptions,
                    final_keywords=final_keywords,
                    draft=draft
                )

            if cms_type == "joomla":
                self.publish_to_joomla(
                    seo_optimized_posts=seo_optimized_posts,
                    seo_optimized_titles=seo_optimized_titles,
                    seo_optimized_metadescriptions=seo_optimized_metadescriptions,
                    final_keywords=final_keywords,
                    draft=draft
                )

            if cms_type == "wix":
                self.publish_to_wix(
                    seo_optimized_posts=seo_optimized_posts,
                    seo_optimized_titles=seo_optimized_titles,
                    seo_optimized_metadescriptions=seo_optimized_metadescriptions,
                    final_keywords=final_keywords,
                    draft=draft
                )
            else:
                print("CMS type not yet recognized.")
        else:
            print("Blog posts were not published to CMS.")
