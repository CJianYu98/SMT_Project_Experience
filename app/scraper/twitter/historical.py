# Import packages
import os
import sys
from datetime import datetime, timedelta
import time

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
    "../../../logs/scraper/twitter/historical_scraper.log",
    format="{time} {file} {level} {message}",
    level="DEBUG",
)

# Constants and variables
S3_BUCKET_NAME = os.getenv("S3_TWITTER_HISTORICAL_BUCKET_NAME")
TIMEZONE = pytz.timezone(os.getenv("TIMEZONE"))

cutoff_days = 1  # Scrape 1 day at a time
start_datetime = datetime.fromtimestamp(1612137599)
stop_datetime = start_datetime - timedelta(days=30) # Change the num days depending on the month
crawl_start_datetime = start_datetime
crawl_stop_datetime = crawl_start_datetime - timedelta(days=cutoff_days)
print(crawl_start_datetime)
print(crawl_stop_datetime)
sg_datetime = datetime.now(TIMEZONE)

tele_start_msg = f"TWITTER HISTORICAL --> Historical data crawling started from {start_datetime.date()} to {stop_datetime.date()} at {sg_datetime}"
tele_end_msg = "TWITTER HISTORICAL --> \n"

os.makedirs("./historical_data", exist_ok=True)

try:
    telegram_send.send(messages=[tele_start_msg])
    logger.info(f"Historical data crawling started from {crawl_start_datetime.date()} to {crawl_stop_datetime.date()} at {sg_datetime}")

    # Scrape 3 days' of data, 1 day at a time
    for i in range(30):
        if i != 0:
            crawl_start_datetime -= timedelta(days=1)
            crawl_stop_datetime -= timedelta(days=1)

        output_file = f"./historical_data/{crawl_start_datetime.date()}_{crawl_stop_datetime.date()}.json"
        s3_object_name = f"{crawl_start_datetime.date()}_{crawl_stop_datetime.date()}.json"

        # Configure Twint
        c = twint.Config()
        c.Near = "Singapore"  # Set geographic location to near Singapore
        c.Lang = "en"  # Set language to english
        c.Limit = sys.maxsize  # Set tweet limit to unlimited
        c.Retweets = True  # Include retweets done by user
        c.Since = str(crawl_stop_datetime.strftime("%Y-%m-%d %H:%M:%S"))  # Set end date for collection
        c.Until = str(crawl_start_datetime.strftime("%Y-%m-%d %H:%M:%S"))  # Set start date for collection
        c.Store_json = True  # Json file format
        c.Output = output_file  # Output file

        twint.run.Search(c)  # Run Twint

        # Intialize S3 client
        s3_client = boto3.client("s3")

        # Upload file to S3 and delete file from local folder afterwards
        try:
            s3_client.upload_file(output_file, S3_BUCKET_NAME, s3_object_name)
            # tele_end_msg += f"File: {output_file} has been uploaded to {S3_BUCKET_NAME}.\n"
            logger.info(f"File: {output_file} has been uploaded to {S3_BUCKET_NAME}.")

            os.remove(output_file)
            # tele_end_msg += f"File: {output_file} removed from local folder successfully.\n"
            logger.info(f"File: {output_file} removed from local folder successfully.")

            telegram_send.send(messages=[f"TWITTER HISTORICAL --> Historical scraping from {crawl_start_datetime.date()} to {crawl_stop_datetime.date()} is completed."])
            logger.info(f"Historical scraping from {crawl_start_datetime.date()} to {crawl_stop_datetime.date()} is completed.")
        except botocore.exceptions.ClientError as s3_error:
            tele_end_msg += f"File: {output_file} failed to upload to {S3_BUCKET_NAME}.\n{s3_error}"
            logger.exception(f"File: {output_file} failed to upload to {S3_BUCKET_NAME}.")
        except Exception as e:
            tele_end_msg += f"Error occured.\n{e}\n"
            logger.exception("Error occured.")
        finally:
            time.sleep(300)
            continue
    tele_end_msg += f"Historical data crawling started from {start_datetime.date()} to {stop_datetime.date()} is fully completed"
    logger.info(f"Historical data crawling started from {start_datetime.date()} to {stop_datetime.date()} is fully completed")
    
except botocore.exceptions.ClientError as aws_error:
    tele_end_msg += f"Error while connecting to AWS S3 client.\n{aws_error}\n"
    logger.exception("Error while connecting to AWS S3 client.")
except Exception as e:
    tele_end_msg += f"Error occured.\n{e}\n"
    logger.exception("Error occured.")
finally:
    telegram_send.send(messages=[tele_end_msg])

