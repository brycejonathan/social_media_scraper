# services/storage.py

import logging
import boto3
import pandas as pd
from io import BytesIO
import os

class StorageService:
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.s3_client = boto3.client('s3')
        self.bucket_name = os.getenv('S3_BUCKET_NAME')
        if not self.bucket_name:
            self.logger.error('S3_BUCKET_NAME environment variable not set.')
            raise ValueError('S3_BUCKET_NAME environment variable not set.')

    def upload_report(self, analysis_results: list) -> str:
        self.logger.info('Uploading report to S3...')
        try:
            df = pd.DataFrame(analysis_results)
            buffer = BytesIO()
            df.to_excel(buffer, index=False)
            buffer.seek(0)

            timestamp = pd.Timestamp.now().strftime('%Y%m%d%H%M%S')
            file_name = f"sentiment_report_{timestamp}.xlsx"

            self.s3_client.put_object(Bucket=self.bucket_name, Key=file_name, Body=buffer.getvalue())

            report_url = f"https://{self.bucket_name}.s3.amazonaws.com/{file_name}"
            self.logger.info(f'Report uploaded successfully. URL: {report_url}')
            return report_url
        except Exception as e:
            self.logger.error(f'Error uploading report to S3: {e}')
            raise
