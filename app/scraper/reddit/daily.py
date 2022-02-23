# Import packages
import json
import math
import os
from datetime import datetime, timedelta

import boto3
import botocore.exceptions
import praw
import pytz
import telegram_send
from dotenv import load_dotenv
from loguru import logger

# Load environment variables
load_dotenv()

# Change to file directory
os.chdir(os.path.dirname(os.path.realpath(__file__)))

# Constants and variables
TIMEZONE = pytz.timezone(os.getenv("TIMEZONE"))
REDDIT_DAILY_DATA_PATH = os.getenv("REDDIT_DAILY_DATA_PATH")
REDDIT_DAILY_LOG_FILE = os.getenv("REDDIT_DAILY_LOG_FILE")
LOG_DIVIDER = "=" * 20

cutoff_days = int(os.getenv("CUTOFF_DAYS"))
start_datetime = datetime.now()
stop_datetime = start_datetime - timedelta(days=cutoff_days)
date = start_datetime.date()
sg_datetime = datetime.now(TIMEZONE)

tele_start_msg = f"REDDIT DAILY --> Daily data crawling started at {sg_datetime}"
tele_end_msg = "REDDIT DAILY --> \n"

subs_dict = {}  # Storage dict
counter = 0  # Post counter for tracking
output_file = f"{REDDIT_DAILY_DATA_PATH}/{date}.json"
s3_object_name = f"{date}.json"

# Add logger configurations
logger.add(
    REDDIT_DAILY_LOG_FILE,
    format="{time} {file} {level} {message}",
    level="DEBUG",
)

try:
    telegram_send.send(messages=[tele_start_msg])
    logger.info(f"{LOG_DIVIDER}\nDaily data crawling started at {sg_datetime}")

    # Intialize S3 client
    s3_client = boto3.client("s3")

    # Access reddit API PRAW
    reddit = praw.Reddit(
        client_id=os.getenv("REDDIT_CLIENT_ID"),
        client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
        user_agent=os.getenv("REDDIT_USER_AGENT"),
        username=os.getenv("REDDIT_USERNAME"),
        password=os.getenv("REDDIT_PASSWORD"),
    )

    # Iterate through list of newest submissions in selected Subreddit
    for sub in reddit.subreddit("Singapore").new(limit=math.inf):

        # Stop loading new posts older than 2 weeks
        # Note that earlier dates are considered smaller than later dates
        # i.e. 2022-01-14 < 2022-01-15
        sub_created_datetime = datetime.fromtimestamp(sub.created_utc)
        if stop_datetime > sub_created_datetime:
            break

        counter += 1  # Increment post counter
        submission = vars(sub)  # Serialize submission into dict format
        submission["comments"] = {}  # Create new comments key-value
        sub.comments.replace_more(limit=None)  # Load comments

        # Loop through list of comments for the submission
        for comment in sub.comments.list():
            comment = vars(comment)
            submission["comments"][comment["id"]] = comment

        subs_dict[submission["id"]] = submission  # Store current submission record

    # Save data to json file
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(subs_dict, f, ensure_ascii=False, indent=4, default=str)
    
    tele_end_msg += f"Reddit daily scraping for {date} completed. {counter} posts scraped."
    logger.info(f"Daily scraping for {date} completed. {counter} posts scraped.")

except praw.exceptions.PRAWException as reddit_error:
    tele_end_msg += f"Error with Reddit API.\n{reddit_error}\n"
    logger.exception("Error with Reddit API.")
except Exception as e:
    tele_end_msg += f"Error occured.\n{e}\n"
    logger.exception("Error occured.")
finally:
    telegram_send.send(messages=[tele_end_msg])
