# tests/test_data_analysis.py

import unittest
from services.data_analysis import DataAnalysisService

class TestDataAnalysisService(unittest.TestCase):
    def setUp(self):
        self.analysis_service = DataAnalysisService()

    def test_analyze_sentiment_positive(self):
        posts = [{'post_id': '1', 'content': 'I love sunny days!'}]
        results = self.analysis_service.analyze_sentiment(posts)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['sentiment_label'], 'Positive')
        self.assertGreater(results[0]['sentiment_score'], 0.1)

    def test_analyze_sentiment_negative(self):
        posts = [{'post_id': '2', 'content': 'I hate rain.'}]
        results = self.analysis_service.analyze_sentiment(posts)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['sentiment_label'], 'Negative')
        self.assertLess(results[0]['sentiment_score'], -0.1)

    def test_analyze_sentiment_neutral(self):
        posts = [{'post_id': '3', 'content': 'It is an average day.'}]
        results = self.analysis_service.analyze_sentiment(posts)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['sentiment_label'], 'Neutral')
        self.assertGreaterEqual(results[0]['sentiment_score'], -0.1)
        self.assertLessEqual(results[0]['sentiment_score'], 0.1)

if __name__ == '__main__':
    unittest.main()
