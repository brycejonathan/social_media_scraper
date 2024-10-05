# services/twitter_api.py

import tweepy
import logging
import os
from typing import List, Dict

class TwitterApi:
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.bearer_token = os.getenv('TWITTER_BEARER_TOKEN')
        if not self.bearer_token:
            self.logger.error('Twitter bearer token not set.')
            raise ValueError('Twitter bearer token not set.')
        self.client = tweepy.Client(bearer_token=self.bearer_token)

    def fetch_posts(self, username: str) -> List[Dict]:
        try:
            user = self.client.get_user(username=username)
            user_id = user.data.id
            tweets = self.client.get_users_tweets(id=user_id, max_results=100, tweet_fields=['created_at'])

            if not tweets.data:
                self.logger.warning(f'No tweets found for user {username}.')
                return []

            posts = []
            for tweet in tweets.data:
                post = {
                    'post_id': tweet.id,
                    'author': username,
                    'content': tweet.text,
                    'created_at': tweet.created_at.isoformat(),
                    'comments': []  # Placeholder for comments
                }
                posts.append(post)
            return posts
        except tweepy.NotFound:
            self.logger.error(f'User {username} not found on Twitter.')
            raise
        except tweepy.TweepyException as e:
            self.logger.error(f'Twitter API error: {e}')
            raise
        except Exception as e:
            self.logger.error(f'Unexpected error: {e}')
            raise
