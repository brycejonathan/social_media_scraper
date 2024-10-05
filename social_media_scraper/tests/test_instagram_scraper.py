# tests/test_instagram_scraper.py

import unittest
from unittest.mock import patch, MagicMock
from services.instagram_scraper import InstagramScraper

class TestInstagramScraper(unittest.TestCase):
    def setUp(self):
        self.scraper = InstagramScraper()

    @patch('requests.get')
    def test_scrape_valid_user(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'graphql': {
                'user': {
                    'edge_owner_to_timeline_media': {
                        'edges': [
                            {
                                'node': {
                                    'id': 'post1',
                                    'edge_media_to_caption': {
                                        'edges': [
                                            {'node': {'text': 'First post'}}
                                        ]
                                    },
                                    'taken_at_timestamp': 1609459200
                                }
                            },
                            {
                                'node': {
                                    'id': 'post2',
                                    'edge_media_to_caption': {
                                        'edges': []
                                    },
                                    'taken_at_timestamp': 1609545600
                                }
                            }
                        ]
                    }
                }
            }
        }
        mock_get.return_value = mock_response

        posts = self.scraper.scrape('valid_user')
        self.assertEqual(len(posts), 2)
        self.assertEqual(posts[0]['post_id'], 'post1')
        self.assertEqual(posts[0]['content'], 'First post')
        self.assertEqual(posts[1]['content'], '')

    @patch('requests.get')
    def test_scrape_invalid_user(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        with self.assertRaises(Exception) as context:
            self.scraper.scrape('invalid_user')
        self.assertIn('Failed to fetch data', str(context.exception))

if __name__ == '__main__':
    unittest.main()
