# tests/test_data_quality.py

import unittest
from services.data_quality import DataQualityService

class TestDataQualityService(unittest.TestCase):
    def setUp(self):
        self.dq_service = DataQualityService()

    def test_validate_posts_all_valid(self):
        posts = [
            {'post_id': '1', 'author': 'user1', 'content': 'Content 1'},
            {'post_id': '2', 'author': 'user2', 'content': 'Content 2'}
        ]
        reports = self.dq_service.validate_posts(posts)
        self.assertEqual(len(reports), 2)
        for report in reports:
            self.assertTrue(report['is_valid'])
            self.assertEqual(len(report['issues']), 0)

    def test_validate_posts_with_issues(self):
        posts = [
            {'post_id': '1', 'author': 'user1'},  # Missing content
            {'author': 'user2', 'content': 'Content 2'},  # Missing post_id
            {'post_id': '3', 'content': 'Content 3'}  # Missing author
        ]
        reports = self.dq_service.validate_posts(posts)
        self.assertEqual(len(reports), 3)
        self.assertFalse(reports[0]['is_valid'])
        self.assertIn('Missing content', reports[0]['issues'])
        self.assertFalse(reports[1]['is_valid'])
        self.assertIn('Missing post_id', reports[1]['issues'])
        self.assertFalse(reports[2]['is_valid'])
        self.assertIn('Missing author', reports[2]['issues'])

if __name__ == '__main__':
    unittest.main()
