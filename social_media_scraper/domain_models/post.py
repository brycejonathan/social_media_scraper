# domain_models/post.py

from dataclasses import dataclass, field
from typing import List
from datetime import datetime
from .comment import Comment

@dataclass
class Post:
    def __init__(self, post_id: str, author: str, content: str, created_at: datetime, comments: List[Comment] = None):
        self.post_id = post_id
        self.author = author
        self.content = content
        self.created_at = created_at
        self.comments = comments if comments is not None else []
