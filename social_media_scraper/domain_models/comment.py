# domain_models/comment.py

from dataclasses import dataclass
from datetime import datetime

@dataclass
class Comment:
    def __init__(self, comment_id: str, author: str, content: str, created_at: datetime):
        self.comment_id = comment_id
        self.author = author
        self.content = content
        self.created_at = created_at
