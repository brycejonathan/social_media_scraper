# services/instagram_scraper.py

import logging
import requests
from typing import List, Dict
from domain_models.post import Post

class InstagramScraper:
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.base_url = "https://www.instagram.com"

    def scrape(self, username: str) -> List[Dict]:
        self.logger.info(f'Starting scrape for Instagram user: {username}')
        try:
            url = f"{self.base_url}/{username}/?__a=1&__d=dis"
            response = requests.get(url)
            if response.status_code != 200:
                self.logger.error(f'Failed to fetch data for {username}. Status Code: {response.status_code}')
                raise Exception(f"Failed to fetch data for account {username}")

            data = response.json()
            posts_data = data.get('graphql', {}).get('user', {}).get('edge_owner_to_timeline_media', {}).get('edges', [])

            if not posts_data:
                self.logger.warning(f'No posts found for Instagram user {username}.')
                return []

            posts = []
            for edge in posts_data:
                node = edge['node']
                post = {
                    'post_id': node['id'],
                    'author': username,
                    'content': node['edge_media_to_caption']['edges'][0]['node']['text'] if node['edge_media_to_caption']['edges'] else '',
                    'created_at': node['taken_at_timestamp'],
                    'comments': []  # Placeholder for comments
                }
                posts.append(post)
            self.logger.info(f'Successfully scraped {len(posts)} posts from Instagram user: {username}')
            return posts
        except requests.RequestException as e:
            self.logger.error(f'Request error while scraping Instagram user {username}: {e}')
            raise
        except Exception as e:
            self.logger.error(f'Unexpected error while scraping Instagram user {username}: {e}')
            raise
