# Import packages
from datetime import datetime, timedelta
import json
import math
import os
import shutil
import telegram_send
import time

import instaloader
import boto3
import botocore.exceptions
import pytz
from dotenv import load_dotenv
from loguru import logger

# Load environment variables
load_dotenv()

# Change to file directory
os.chdir(os.path.dirname(os.path.realpath(__file__)))

# Add logger configurations
logger.add(
    "../../../logs/scraper/instagram/daily_scraper.log",
    format="{time} {file} {level} {message}",
    level="DEBUG",
)

# Constants and variables
ACCOUNT = os.getenv("INSTAGRAM_ACCOUNT")
PASSWORD = os.getenv("INSTAGRAM_PASSWORD")
S3_BUCKET_NAME = os.getenv("S3_INSTA_DAILY_BUCKET_NAME")
TIMEZONE = pytz.timezone(os.getenv("TIMEZONE"))

cutoff_days = int(os.getenv("CUTOFF_DAYS"))
start_datetime = datetime.now()
stop_datetime = start_datetime - timedelta(days=cutoff_days)
date = start_datetime.date()
sg_datetime = datetime.now(TIMEZONE)

tele_start_msg = f"INSTA DAILY --> Daily data crawling started at {sg_datetime}"
tele_end_msg = "INSTA DAILY --> \n"


try:
    telegram_send.send(messages=[tele_start_msg])
    logger.info(f"Daily data crawling started at {sg_datetime}")

    # Intialize S3 client
    s3_client = boto3.client("s3")

    # Create an instance of Instaloader class and login
    loader = instaloader.Instaloader(compress_json=False, download_comments=True, quiet=True)
    loader.login(ACCOUNT, PASSWORD)

    # Get profiles to scrape
    profiles = json.load(open('../accounts_to_scrape/instagram.json'))

    # Change to data directory where data will be downloaded
    os.makedirs('./data', exist_ok=True)
    os.chdir('./data')

    # Iterate through profiles
    for p in profiles.values():
        # Get profile object
        try: 
            profile = instaloader.Profile.from_username(loader.context, p)

            # Get all posts from the profile in a generator
            posts = profile.get_posts()

            for post in posts:
                # Download post if it is within 2 weeks
                if post.date_local <= stop_datetime:
                    break
                
                loader.download_post(post, target=f"@{p}")
                time.sleep(3)
            logger.info(f'Posts for @{p} scraped.')

            # Upload all files for a profile to AWS S3
            logger.info(os.getcwd())
            if os.path.isdir(f"./@{p}"):
                for file in os.listdir(f'./@{p}'):
                    s3_object_name = f'{date}/@{p}/{file}'
                    s3_client.upload_file(f"./@{p}/{file}", S3_BUCKET_NAME, s3_object_name)
                logger.info(f'Files for @{p} successfully uploaded to AWS S3.')

                # Remove directory after uploading files to AWS S3
                shutil.rmtree(f'./@{p}')
                logger.info(f'Directory @{p} successfully deleted from local directory.')

        except Exception as e:
            telegram_send.send(messages=[f"INSTA DAILY --> Error: {e}\nContinuing on..."])
            logger.exception(f"Error: {e}\nContinuing on...")
            continue
        telegram_send.send(messages=[f"INSTA DAILY --> @{p} profile scraped successfully."])
        time.sleep(30)

    tele_end_msg += f'Daily scraper completed for {date}.'

except Exception as e:
    tele_end_msg += f"Error occured.\n{e}\n"
    logger.exception("Error occured.")
finally:
    telegram_send.send(messages=[tele_end_msg])
