# services/data_quality.py

import logging
from typing import List, Dict
from domain_models.data_quality_report import DataQualityReport

class DataQualityService:
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)

    def validate_posts(self, posts: List[Dict]) -> List[Dict]:
        self.logger.info('Starting data quality validation...')
        reports = []
        for post in posts:
            issues = []
            if not post.get('post_id'):
                issues.append('Missing post_id')
            if not post.get('content'):
                issues.append('Missing content')
            if not post.get('author'):
                issues.append('Missing author')
            is_valid = len(issues) == 0
            report = {
                'report_id': f"RPT-{post.get('post_id')}",
                'post_id': post.get('post_id'),
                'is_valid': is_valid,
                'issues': issues
            }
            reports.append(report)
            if not is_valid:
                self.logger.warning(f"Post {post.get('post_id')} failed validation: {issues}")
        self.logger.info('Data quality validation completed.')
        return reports
