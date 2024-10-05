# services/data_analysis.py

import logging
from typing import List, Dict
from textblob import TextBlob

class DataAnalysisService:
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)

    def analyze_sentiment(self, posts: List[Dict]) -> List[Dict]:
        self.logger.info('Starting sentiment analysis...')
        results = []
        for post in posts:
            content = post.get('content', '')
            if not content:
                self.logger.warning(f'Post {post.get("post_id")} has empty content. Skipping sentiment analysis.')
                continue
            analysis = TextBlob(content)
            sentiment_score = analysis.sentiment.polarity
            sentiment_label = self.get_sentiment_label(sentiment_score)
            result = {
                'analysis_id': f"ANA-{post.get('post_id')}",
                'post_id': post.get('post_id'),
                'sentiment_score': sentiment_score,
                'sentiment_label': sentiment_label
            }
            results.append(result)
            self.logger.debug(f"Post {post.get('post_id')} - Score: {sentiment_score}, Label: {sentiment_label}")
        self.logger.info('Sentiment analysis completed.')
        return results

    def get_sentiment_label(self, score: float) -> str:
        if score > 0.1:
            return 'Positive'
        elif score < -0.1:
            return 'Negative'
        else:
            return 'Neutral'
