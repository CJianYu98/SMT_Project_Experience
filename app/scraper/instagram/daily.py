# Import packages
from datetime import datetime, timedelta
import json
import math
import os
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

# Constants and variables
ACCOUNT = os.getenv("INSTAGRAM_ACCOUNT")
PASSWORD = os.getenv("INSTAGRAM_PASSWORD")

cutoff_days = int(os.getenv("CUTOFF_DAYS"))
start_datetime = datetime.now()
stop_datetime = start_datetime - timedelta(days=cutoff_days)
date = start_datetime.date()
sg_datetime = datetime.now(TIMEZONE)

tele_start_msg = f"INSTAGRAM DAILY --> Daily data crawling started at {sg_datetime}"
tele_end_msg = "INSTAGRAM DAILY --> \n"


try:
    telegram_send.send(messages=[tele_start_msg])
    logger.info(f"Daily data crawling started at {sg_datetime}")

    # Create an instance of Instaloader class and login
    loader = instaloader.Instaloader(compress_json=False, download_comments=True, quiet=True)
    loader.login(ACCOUNT, PASSWORD)

    # Get profiles to scrape
    profiles = json.load(open('../accounts_to_scrape/instagram.json'))

    # Change to data directory where data will be downloaded
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
            logger.debug(f'Posts for @{p} scraped.')
        except Exception as e:
            telegram_send.send(messages=[f"Error: {e}\nContinuing on..."])
            logger.debug("Error: {e}\nContinuing on...")
            continue
    
    tele_end_msg += f'Daily scraper completed for {date}.'

except Exception as e:
    tele_end_msg += f"Error occured.\n{e}\n"
    logger.exception("Error occured.")

telegram_send.send(messages=[tele_end_msg])
