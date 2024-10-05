# lambda_function/lambda_handler.py

import json
import logging
import os
from services.twitter_scraper import TwitterScraper
from services.instagram_scraper import InstagramScraper
from services.data_quality import DataQualityService
from services.data_analysis import DataAnalysisService
from services.storage import StorageService
from api.api import Api
from logging_config import setup_logging

def lambda_handler(event, context):
    setup_logging()
    logger = logging.getLogger('LambdaHandler')

    try:
        logger.info('Received event: %s', json.dumps(event))

        # Extract profile URL from the event
        profile_url = event.get('profile_url')
        if not profile_url:
            logger.error('No profile_url provided in the event.')
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'No profile_url provided.'})
            }

        from urllib.parse import urlparse
        parsed_url = urlparse(profile_url)
        platform = None
        username = None

        if 'twitter.com' in parsed_url.netloc:
            platform = 'twitter'
            username = parsed_url.path.strip('/')
        elif 'instagram.com' in parsed_url.netloc:
            platform = 'instagram'
            username = parsed_url.path.strip('/')
        else:
            logger.error('Unsupported platform. Please provide a Twitter or Instagram profile URL.')
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Unsupported platform. Choose "twitter" or "instagram".'})
            }

        logger.info(f'Platform: {platform.capitalize()}, Username: {username}')

        # Scraping
        if platform == 'twitter':
            scraper = TwitterScraper()
        elif platform == 'instagram':
            scraper = InstagramScraper()
        else:
            logger.error('Unsupported platform.')
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Unsupported platform.'})
            }

        logger.info('Starting scraping...')
        posts = scraper.scrape(username)
        logger.info(f'Scraped {len(posts)} posts.')

        # Data Quality
        dq_service = DataQualityService()
        logger.info('Validating data quality...')
        quality_reports = dq_service.validate_posts(posts)
        valid_posts = [post for post, report in zip(posts, quality_reports) if report['is_valid']]
        logger.info(f'{len(valid_posts)} posts passed data quality checks.')

        # Data Analysis
        analysis_service = DataAnalysisService()
        logger.info('Analyzing sentiment...')
        analysis_results = analysis_service.analyze_sentiment(valid_posts)
        logger.info('Sentiment analysis completed.')

        # Storage
        storage_service = StorageService()
        logger.info('Uploading report to S3...')
        report_url = storage_service.upload_report(analysis_results)
        logger.info(f'Report uploaded successfully. URL: {report_url}')

        # API Interaction (if needed)
        api = Api()
        api.notify_completion(username, platform, report_url)

        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Scraping and analysis completed successfully.', 'report_url': report_url})
        }

    except Exception as e:
        logger.exception(f'An error occurred: {e}')
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
