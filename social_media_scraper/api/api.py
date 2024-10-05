# api/api.py

from flask import Flask, request, jsonify, send_file
import logging
import boto3
import os
import json
from io import BytesIO

app = Flask(__name__)
logger = logging.getLogger('Api')
logger.setLevel(logging.INFO)

# Initialize AWS services
sqs_client = boto3.client('sqs')
sns_client = boto3.client('sns')
s3_client = boto3.client('s3')

queue_url = os.getenv('SCRAPE_QUEUE_URL')
sns_topic_arn = os.getenv('SNS_TOPIC_ARN')
bucket_name = os.getenv('S3_BUCKET_NAME')

@app.route('/start-scraping', methods=['POST'])
def start_scraping():
    try:
        data = request.get_json()
        account = data.get('account')
        platform = data.get('platform')

        if not account or not platform:
            logger.error('Missing account or platform in request.')
            return jsonify({'error': 'Missing account or platform'}), 400

        if platform.lower() not in ['twitter', 'instagram']:
            logger.error('Unsupported platform requested.')
            return jsonify({'error': 'Unsupported platform. Choose "twitter" or "instagram".'}), 400

        message = {
            'account': account,
            'platform': platform.lower()
        }

        response = sqs_client.send_message(
            QueueUrl=queue_url,
            MessageBody=json.dumps(message)
        )

        logger.info(f'Scraping task initiated for {platform} account: {account}. Message ID: {response["MessageId"]}')

        return jsonify({'message': 'Scraping task initiated.', 'message_id': response['MessageId']}), 200

    except Exception as e:
        logger.exception('Error initiating scraping task.')
        return jsonify({'error': str(e)}), 500

@app.route('/status/<task_id>', methods=['GET'])
def get_status(task_id):
    try:
        # Placeholder for actual status retrieval logic
        # This could involve querying a database or tracking system
        status = 'In Progress'  # Example status

        logger.info(f'Retrieved status for task ID: {task_id}')

        return jsonify({'task_id': task_id, 'status': status}), 200

    except Exception as e:
        logger.exception('Error retrieving task status.')
        return jsonify({'error': str(e)}), 500

@app.route('/reports/<report_id>', methods=['GET'])
def get_report(report_id):
    try:
        # Fetch the report from S3
        file_key = f"sentiment_report_{report_id}.xlsx"
        response = s3_client.get_object(Bucket=bucket_name, Key=file_key)
        file_content = response['Body'].read()

        logger.info(f'Retrieved report {report_id} from S3.')

        return send_file(
            BytesIO(file_content),
            attachment_filename=file_key,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )

    except s3_client.exceptions.NoSuchKey:
        logger.error(f'Report {report_id} not found.')
        return jsonify({'error': 'Report not found.'}), 404
    except Exception as e:
        logger.exception('Error retrieving report.')
        return jsonify({'error': str(e)}), 500

@app.route('/notify', methods=['POST'])
def notify_completion():
    try:
        data = request.get_json()
        username = data.get('username')
        platform = data.get('platform')
        report_url = data.get('report_url')

        if not username or not platform or not report_url:
            logger.error('Missing username, platform, or report_url in request.')
            return jsonify({'error': 'Missing username, platform, or report_url'}), 400

        message = f"Scraping and analysis completed for {platform.capitalize()} account '{username}'.\nReport URL: {report_url}"
        subject = f"Scraping Report for {platform.capitalize()} - {username}"

        response = sns_client.publish(
            TopicArn=sns_topic_arn,
            Message=message,
            Subject=subject
        )

        logger.info(f'Notification sent. Message ID: {response["MessageId"]}')

        return jsonify({'message': 'Notification sent.', 'message_id': response['MessageId']}), 200

    except Exception as e:
        logger.exception('Error sending notification.')
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Enable debug mode for development; disable in production
    app.run(host='0.0.0.0', port=5000, debug=True)
