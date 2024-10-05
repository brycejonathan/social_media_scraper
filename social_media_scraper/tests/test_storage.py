# tests/test_storage.py

import unittest
from unittest.mock import patch, MagicMock
from services.storage import StorageService

class TestStorageService(unittest.TestCase):
    def setUp(self):
        self.storage_service = StorageService()

    @patch('boto3.client')
    def test_upload_report_success(self, mock_boto_client):
        mock_s3 = MagicMock()
        mock_boto_client.return_value = mock_s3

        analysis_results = [
            {'analysis_id': 'ANA-1', 'post_id': '1', 'sentiment_score': 0.5, 'sentiment_label': 'Positive'},
            {'analysis_id': 'ANA-2', 'post_id': '2', 'sentiment_score': -0.3, 'sentiment_label': 'Negative'}
        ]

        report_url = self.storage_service.upload_report(analysis_results)
        self.assertIn('https://', report_url)
        mock_s3.put_object.assert_called_once()

    @patch('boto3.client')
    def test_upload_report_failure(self, mock_boto_client):
        mock_s3 = MagicMock()
        mock_s3.put_object.side_effect = Exception('S3 Upload Failed')
        mock_boto_client.return_value = mock_s3

        analysis_results = [
            {'analysis_id': 'ANA-1', 'post_id': '1', 'sentiment_score': 0.5, 'sentiment_label': 'Positive'}
        ]

        with self.assertRaises(Exception) as context:
            self.storage_service.upload_report(analysis_results)
        self.assertIn('S3 Upload Failed', str(context.exception))

if __name__ == '__main__':
    unittest.main()
