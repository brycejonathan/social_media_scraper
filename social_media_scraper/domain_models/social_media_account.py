# domain_models/social_media_account.py

from dataclasses import dataclass

@dataclass
class SocialMediaAccount:
    def __init__(self, platform: str, username: str, account_id: str):
        self.platform = platform  # 'Twitter' or 'instagram'
        self.username = username
        self.account_id = account_id
