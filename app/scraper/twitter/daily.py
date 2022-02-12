# Import packages
import os
import sys
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

# Change to file directory
os.chdir(os.path.dirname(os.path.realpath(__file__)))

# Add logger configurations
logger.add(
    "../../../logs/scraper/twitter/daily_scraper.log",
    format="{time} {file} {level} {message}",
    level="DEBUG",
)

# Constants and variables
S3_BUCKET_NAME = os.getenv("S3_TWITTER_DAILY_BUCKET_NAME")
TIMEZONE = pytz.timezone(os.getenv("TIMEZONE"))

cutoff_days = int(os.getenv("CUTOFF_DAYS")) - 11  # Only scrape past 3 days for twitter
start_datetime = datetime.now()
stop_datetime = start_datetime - timedelta(days=cutoff_days)
date = start_datetime.date()
sg_datetime = datetime.now(TIMEZONE)

tele_start_msg = f"TWITTER DAILY --> Daily data crawling started at {sg_datetime}"
tele_end_msg = "TWITTER DAILY --> \n"
output_file = f"./daily_data/{start_datetime.date()}.json"
s3_object_name = f"{date}.json"

try:
    telegram_send.send(messages=[tele_start_msg])
    logger.info(f"Daily data crawling started at {sg_datetime}")

    # Configure Twint
    c = twint.Config()
    c.Near = "Singapore"  # Set geographic location to near Singapore
    c.Lang = "en"  # Set language to english
    c.Limit = sys.maxsize  # Set tweet limit to unlimited
    c.Retweets = True  # Include retweets done by user
    c.Since = str(stop_datetime.strftime("%Y-%m-%d %H:%M:%S"))  # Set end date for collection
    c.Until = str(start_datetime.strftime("%Y-%m-%d %H:%M:%S"))  # Set start date for collection
    c.Store_json = True  # Json file format
    c.Output = output_file  # Output file

    twint.run.Search(c)  # Run Twint

    # Intialize S3 client
    s3_client = boto3.client("s3")

    # Upload file to S3 and delete file from local folder afterwards
    try:
        s3_client.upload_file(output_file, S3_BUCKET_NAME, s3_object_name)
        tele_end_msg += f"File: {output_file} has been uploaded to {S3_BUCKET_NAME}.\n"
        logger.info(f"File: {output_file} has been uploaded to {S3_BUCKET_NAME}.")

        os.remove(output_file)
        tele_end_msg += f"File: {output_file} removed from local folder successfully.\n"
        logger.info(f"File: {output_file} removed from local folder successfully.")

        tele_end_msg += f"Twitter daily scraping for {date} completed. {counter} posts scraped."
        logger.info(f"Daily scraping for {date} completed. {counter} posts scraped.")
    except botocore.exceptions.ClientError as s3_error:
        tele_end_msg += f"File: {output_file} failed to upload to {S3_BUCKET_NAME}.\n{s3_error}"
        logger.exception(f"File: {output_file} failed to upload to {S3_BUCKET_NAME}.")
    except Exception as e:
        tele_end_msg += f"Error occured.\n{e}\n"
        logger.exception("Error occured.")


except botocore.exceptions.ClientError as aws_error:
    tele_end_msg += f"Error while connecting to AWS S3 client.\n{aws_error}\n"
    logger.exception("Error while connecting to AWS S3 client.")
except Exception as e:
    tele_end_msg += f"Error occured.\n{e}\n"
    logger.exception("Error occured.")
finally:
    telegram_send.send(messages=[tele_end_msg])
