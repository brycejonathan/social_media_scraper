# services/twitter_scraper.py

import logging
from typing import List, Dict
from domain_models.post import Post
from services.twitter_api import TwitterApi

class TwitterScraper:
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.api = TwitterApi()

    def scrape(self, username: str) -> List[Dict]:
        self.logger.info(f'Starting scrape for Twitter user: {username}')
        try:
            posts_data = self.api.fetch_posts(username)
            self.logger.info(f'Successfully fetched {len(posts_data)} posts.')
            return posts_data
        except Exception as e:
            self.logger.error(f'Error scraping Twitter user {username}: {e}')
            raise
