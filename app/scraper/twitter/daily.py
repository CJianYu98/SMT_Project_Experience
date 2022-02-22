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
DATA_FOLDER = "./daily_data"
LOG_DIVIDER = "=" * 20

start_datetime = datetime.now()
stop_datetime = start_datetime - timedelta(days=1)
date = start_datetime.date()
sg_datetime = datetime.now(TIMEZONE)

tele_start_msg = f"TWITTER DAILY --> Daily data crawling started at {sg_datetime}"
tele_end_msg = "TWITTER DAILY --> \n"

# Create temp folder to store scraped data
os.makedirs(f"./{DATA_FOLDER}", exist_ok=True)

try:
    telegram_send.send(messages=[tele_start_msg])
    logger.info(f"{LOG_DIVIDER}\nDaily data crawling started at {sg_datetime}")

    # Scrape 7 days' of data, 1 day at a time
    for i in range(7):
        if i != 0:
            start_datetime -= timedelta(days=1)
            stop_datetime -= timedelta(days=1)

        output_file = f"./daily_data/{date}_{i+1}.json"
        s3_object_name = f"{date}/{start_datetime.date()}.json"

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

            telegram_send.send(
                messages=[
                    f"TWITTER DAILY --> Daily scraping for {date}: ({i}) - {start_datetime.date()} data completed."
                ]
            )
            logger.info(f"Daily scraping for {date}: {start_datetime.date()} data completed.")
        except botocore.exceptions.ClientError as s3_error:
            tele_end_msg += f"File: {output_file} failed to upload to {S3_BUCKET_NAME}.\n{s3_error}"
            logger.exception(f"File: {output_file} failed to upload to {S3_BUCKET_NAME}.")
        except Exception as e:
            tele_end_msg += f"Error occured.\n{e}\n"
            logger.exception("Error occured.")
        finally:
            time.sleep(300)
            continue
    tele_end_msg += f"Twitter daily scraping for {date} is fully completed."
    logger.info(f"Daily craping for {date} is fully completed.")

except botocore.exceptions.ClientError as aws_error:
    tele_end_msg += f"Error while connecting to AWS S3 client.\n{aws_error}\n"
    logger.exception("Error while connecting to AWS S3 client.")
except Exception as e:
    tele_end_msg += f"Error occured.\n{e}\n"
    logger.exception("Error occured.")
finally:
    telegram_send.send(messages=[tele_end_msg])

# Add logger configurations
logger.add(
    "../../../logs/scraper/reddit/historical_scraper.log",
    format="{time} {file} {level} {message}",
    level="DEBUG",
)


def monthly_crawl_submissions():
    # Constants
    TIMEZONE = pytz.timezone(os.getenv("TIMEZONE"))
    last_created_utc = 1577836800  # 2020-01-01 00:00:00
    cutoff_date = 1609459200  # 2021-01-01 00:00:00
    run = True

    OUTPUT_DIR = "./data"
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    telegram_send.send(
        messages=[
            f"REDDIT HISTORICAL --> Submissions crawling for 2020-2021 started at {datetime.now(TIMEZONE)}"
        ]
    )

    # Start scraping from given date
    while run:
        logger.debug(f"last_created_utc: {last_created_utc}")
        params = {
            "subreddit": "singapore",
            "sort": "asc",
            "metadata": "true",
            "after": last_created_utc,
            "size": 100,  # Max 500
        }

        try:
            response = requests.get(
                "https://api.pushshift.io/reddit/search/submission/", params=params
            )
            if response.status_code == 200:
                jobj = json.loads(response.text)
                if jobj.get("data"):
                    for submission in jobj.get("data"):
                        created_utc = submission["created_utc"]
                        if datetime.fromtimestamp(
                            created_utc, timezone.utc
                        ) > datetime.fromtimestamp(cutoff_date, timezone.utc):
                            run = False
                            break

                        yyyymm = datetime.fromtimestamp(created_utc, timezone.utc).strftime("%Y%m")
                        with open(f"{OUTPUT_DIR}/{yyyymm}.jsonl", "a") as fo:
                            fo.write(json.dumps(submission) + "\n")

                    logger.debug(f"Data size: {len(jobj.get('data'))}")
                    last_created_utc = jobj["data"][-1]["created_utc"]

                    time.sleep(3)
                else:
                    logger.debug("No data in submission object.")
                    break

        except Exception as e:
            logger.exception(e)
            telegram_send.send(messages=[f"Error occured, retrying.\n{e}"])
            time.sleep(15)
            continue
    logger.debug("Submissions crawling complete.")
    telegram_send.send(
        messages=["REDDIT HISTORICAL --> Submissions crawling for 2020-2021 is completed."]
    )
