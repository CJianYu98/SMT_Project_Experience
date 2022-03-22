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

# Load environment variables
load_dotenv()

# Constants
TWITTER_DAILY_DATA_PATH = os.getenv("TWITTER_DAILY_DATA_PATH")
TWITTER_DAILY_ETL_LOG_FILE = os.getenv("TWITTER_DAILY_ETL_LOG_FILE")
DB_TWIITER_TWEETS_COLLECTION = os.getenv("DB_TWIITER_TWEETS_COLLECTION")
DB_TWITTER_COMMENTS_COLLECTION = os.getenv("DB_TWITTER_COMMENTS_COLLECTION")
SG_TIMEZONE = pytz.timezone('Asia/Singapore')

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
curr_date = datetime.now(SG_TIMEZONE).date()

if latest_collection_date.date() == curr_date:
    logger.info(f"Starting daily ETL Twitter {file} in GPU server")
    tele.send(messages=[f"Starting daily ETL Twitter {file} in GPU server"])

    end_date = datetime.strptime(latest_collection_date, "%Y-%m-%d")
    start_date = end_date - timedelta(days=7)
    db_query = {"date": {"$gte": start_date, "$lte": end_date}}
    twitter_tweets.delete_many(db_query)
    twitter_comments.delete_many(db_query)

    files = sorted(os.listdir(f"{TWITTER_DAILY_DATA_PATH}/{latest_collection_date}"))

    for file in files:
        logger.info(f"Processing {file}")
        df = pd.read_json(f"{TWITTER_DAILY_DATA_PATH}/{latest_collection_date}/{file}", orient='records', lines=True)

        df_en = df[df['language'] == 'en']
        df_filtered = df_en[TWITTER_DAILY_TWEET_FIELDS]

        df_tweets = df_filtered.loc[df_filtered['reply_to'].isin([[]])].reset_index()
        df_comments = df_filtered[df_filtered['reply_to'].isin([[]]) == False].reset_index()
        df_comments['parent_id'] = df_comments["reply_to"].apply(lambda x: int(x[0]['id']))

        tweets = df_tweets.to_dict(orient="index")
        comments = df_comments.to_dict(orient="index")

        twitter_tweets.insert_many([tweets[i] for i in range(len(tweets))])
        twitter_comments.insert_many([comments[i] for i in range(len(comments))])

        logger.info(f"{file} processed")

    tele.send(messages=[f"Daily ETL for Twitter completed"])