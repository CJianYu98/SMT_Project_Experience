import json
import os
import time
from datetime import datetime, timedelta
from pprint import pprint

import pandas as pd
import pytz
import telegram_send as tele
from dotenv import load_dotenv
from loguru import logger

from ..constants.social_media import (
    TWITTER_DAILY_TWEET_FIELDS,
    TWITTER_DAILY_COMMENT_FIELDS,
)
from .connect import db
from .status_check import check_status

# Load environment variables
load_dotenv()

# Constants
TWITTER_DAILY_DATA_PATH = os.getenv("TWITTER_DAILY_DATA_PATH")
TWITTER_DAILY_ETL_LOG_FILE = os.getenv("TWITTER_DAILY_ETL_LOG_FILE")
DB_TWIITER_TWEETS_COLLECTION = os.getenv("DB_TWIITER_TWEETS_COLLECTION")
DB_TWITTER_COMMENTS_COLLECTION = os.getenv("DB_TWITTER_COMMENTS_COLLECTION")
SG_TIMEZONE = pytz.timezone('Asia/Singapore')
STATUS_CHECK_FILE = os.getenv("STATUS_CHECK_FILE")

# Add logger configurations
logger.add(
    TWITTER_DAILY_ETL_LOG_FILE,
    format="{time} {file} {level} {message}",
    level="DEBUG",
)

# Select MongoDB collection to work with
twitter_tweets = db[DB_TWIITER_TWEETS_COLLECTION]
twitter_comments = db[DB_TWITTER_COMMENTS_COLLECTION]

# Check status for reddit daily collection
status_file = open(STATUS_CHECK_FILE)
status_jobj = json.load(status_file)
latest_collection_date = datetime.strptime(
    status_jobj["twitter"]["latest_collection_date"], "%Y-%m-%d"
)
latest_etl_date = datetime.strptime(
    status_jobj["twitter"]["latest_etl_date"], "%Y-%m-%d"
)
curr_date = datetime.now(SG_TIMEZONE).date()

if (latest_collection_date.date() == curr_date) and (latest_etl_date.date() < latest_collection_date.date()):
    start = time.time()
    logger.info(f"Starting daily ETL Twitter {latest_collection_date.date()} in GPU server")
    tele.send(messages=[f"Starting daily ETL Twitter {latest_collection_date.date()} in GPU server"])

    # Delete all tweets within date range
    end_date = latest_collection_date
    start_date = end_date - timedelta(days=7)
    db_query = {"date": {"$gte": start_date, "$lte": end_date}}
    twitter_tweets.delete_many(db_query)
    twitter_comments.delete_many(db_query)

    # Get all data files for the day of scraping
    files = sorted(os.listdir(f"{TWITTER_DAILY_DATA_PATH}/{latest_collection_date.date()}"))

    for file in files:
        logger.info(f"Processing {file}")

        # Read in json date file for each date
        df = pd.read_json(f"{TWITTER_DAILY_DATA_PATH}/{latest_collection_date.date()}/{file}", orient='records', lines=True)

        # Filtered unwanted data and data columns
        df_en = df[df['language'] == 'en']
        df_filtered = df_en[TWITTER_DAILY_TWEET_FIELDS]

        # Spilt data in tweets and comments
        df_tweets = df_filtered.loc[df_filtered['reply_to'].isin([[]])].reset_index()
        df_comments = df_filtered[df_filtered['reply_to'].isin([[]]) == False].reset_index()
        df_comments['parent_id'] = df_comments["reply_to"].apply(lambda x: int(x[0]['id']))

        # Convert df to dict format
        tweets = df_tweets.to_dict(orient="index")
        comments = df_comments.to_dict(orient="index")

        # Insert tweets and comments into their respective db collection
        twitter_tweets.insert_many([tweets[i] for i in range(len(tweets))])
        twitter_comments.insert_many([comments[i] for i in range(len(comments))])

        logger.info(f"{file} processed")

    # Update status file
    status_jobj['twitter']['latest_etl_date'] = datetime.now().date().strftime("%Y-%m-%d")
    with open(STATUS_CHECK_FILE, 'w') as f:
        json.dump(status_jobj, f, indent=4)

    duration = time.time() - start
    logger.info(f"Daily ETL for Twitter in GPU server completed, time taken: {duration}")
    tele.send(messages=[f"Daily ETL for Twitter in GPU server completed, time taken: {duration}"])