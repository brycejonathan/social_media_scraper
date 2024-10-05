# domain_models/sentiment_analysis.py

from dataclasses import dataclass

@dataclass
class SentimentAnalysis:
    def __init__(self, analysis_id: str, post_id: str, sentiment_score: float, sentiment_label: str):
        self.analysis_id = analysis_id
        self.post_id = post_id
        self.sentiment_score = sentiment_score
        self.sentiment_label = sentiment_label  # e.g., 'Positive', 'Negative', 'Neutral'
