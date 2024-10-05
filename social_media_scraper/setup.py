# setup.py

from setuptools import setup, find_packages

setup(
    name='social_media_scraper',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        'tweepy==4.10.1',
        'requests==2.28.1',
        'textblob==0.17.1',
        'boto3==1.26.0',
        'pandas==1.5.3',
        'openpyxl==3.1.2',
        'flask==2.2.5',
        'click==8.1.3'
    ],
    entry_points={
        'console_scripts': [
            'social-scraper=cli.main:main'
        ]
    },
    author='Your Name',
    author_email='your.email@example.com',
    description='A CLI tool for scraping social media data from Twitter and Instagram.',
    url='https://github.com/yourusername/social_media_scraper',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
)
