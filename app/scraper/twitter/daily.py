# Import packages
import os
import sys
import time
from datetime import datetime, timedelta

import boto3
import botocore.exceptions
import pytz
import telegram_send
import twint
from dotenv import load_dotenv
from loguru import logger

# Load environment variables
load_dotenv()

# Constants and variables
S3_BUCKET_NAME = os.getenv("S3_TWITTER_DAILY_BUCKET_NAME")
TIMEZONE = pytz.timezone(os.getenv("TIMEZONE"))
TWITTER_DAILY_DATA_PATH = os.getenv("TWITTER_DAILY_DATA_PATH")
TWITTER_DAILY_LOG_FILE = os.getenv("TWITTER_DAILY_LOG_PATH")
LOG_DIVIDER = "=" * 20

start_datetime = datetime.now()
stop_datetime = start_datetime - timedelta(days=1)
date = start_datetime.date()
sg_datetime = datetime.now(TIMEZONE)

tele_start_msg = f"TWITTER DAILY --> Daily data crawling started at {sg_datetime}"
tele_end_msg = "TWITTER DAILY --> \n"

# Add logger configurations
logger.add(
    TWITTER_DAILY_LOG_FILE,
    format="{time} {file} {level} {message}",
    level="DEBUG",
)

# Create folder to store scraped data
os.makedirs(f"{TWITTER_DAILY_DATA_PATH}/{date}", exist_ok=True)

try:
    telegram_send.send(messages=[tele_start_msg])
    logger.info(f"{LOG_DIVIDER}\nDaily data crawling started at {sg_datetime}")

    # Scrape 7 days' of data, 1 day at a time
    for i in range(7):
        if i != 0:
            start_datetime -= timedelta(days=1)
            stop_datetime -= timedelta(days=1)

        output_file = f"{TWITTER_DAILY_DATA_PATH}/{date}/{date}_{i+1}.json"

        # Configure Twint
        c = twint.Config()
        c.Near = "Singapore"  # Set geographic location to near Singapore
        c.Lang = "en"  # Set language to english
        c.Limit = sys.maxsize  # Set tweet limit to unlimited
        c.Retweets = True  # Include retweets done by user
        c.Since = str(stop_datetime.strftime("%Y-%m-%d %H:%M:%S"))  # Set end date
        c.Until = str(start_datetime.strftime("%Y-%m-%d %H:%M:%S"))  # Set start date
        c.Store_json = True  # Json file format
        c.Output = output_file  # Output file

        twint.run.Search(c)  # Run Twint

        telegram_send.send(
            messages=[
                f"TWITTER DAILY --> Daily scraping for {date}: ({i}) - {start_datetime.date()} data completed."
            ]
        )
        logger.info(f"Daily scraping for {date}: {start_datetime.date()} data completed.")

        # Wait for 5 minutes to prevent request limit
        time.sleep(300)
        
    tele_end_msg += f"Twitter daily scraping for {date} is fully completed."
    logger.info(f"Daily craping for {date} is fully completed.")

except Exception as e:
    tele_end_msg += f"Error occured.\n{e}\n"
    logger.exception("Error occured.")
finally:
    telegram_send.send(messages=[tele_end_msg])