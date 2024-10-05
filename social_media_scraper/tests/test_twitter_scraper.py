# tests/test_twitter_scraper.py

import unittest
from unittest.mock import patch, MagicMock
from services.twitter_scraper import TwitterScraper

class TestTwitterScraper(unittest.TestCase):
    def setUp(self):
        self.scraper = TwitterScraper()

    @patch('services.twitter_api.TwitterApi.fetch_posts')
    def test_scrape_valid_user(self, mock_fetch_posts):
        mock_fetch_posts.return_value = [
            {'post_id': '1', 'author': 'user1', 'content': 'Hello World!', 'created_at': '2023-10-04T12:00:00Z'},
            {'post_id': '2', 'author': 'user1', 'content': 'Another tweet', 'created_at': '2023-10-05T13:30:00Z'}
        ]
        posts = self.scraper.scrape('user1')
        self.assertEqual(len(posts), 2)
        self.assertEqual(posts[0]['post_id'], '1')
        self.assertEqual(posts[0]['author'], 'user1')
        self.assertEqual(posts[0]['content'], 'Hello World!')

    @patch('services.twitter_api.TwitterApi.fetch_posts')
    def test_scrape_invalid_user(self, mock_fetch_posts):
        mock_fetch_posts.side_effect = Exception('User not found')
        with self.assertRaises(Exception):
            self.scraper.scrape('invalid_user')

if __name__ == '__main__':
    unittest.main()
