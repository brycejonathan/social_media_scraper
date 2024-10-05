# domain_models/data_quality_report.py

from dataclasses import dataclass
from typing import List

@dataclass
class DataQualityReport:
    def __init__(self, report_id: str, post_id: str, is_valid: bool, issues: List[str]):
        self.report_id = report_id
        self.post_id = post_id
        self.is_valid = is_valid
        self.issues = issues
