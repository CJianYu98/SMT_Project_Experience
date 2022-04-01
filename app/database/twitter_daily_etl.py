import json
import os
from datetime import datetime, timedelta
from pprint import pprint
from time import time

import pandas as pd
import pytz
import telegram_send as tele
from dotenv import load_dotenv
from loguru import logger

from ..constants.etl import get_time
from ..constants.social_media import (
    TWITTER_DAILY_COMMENT_FIELDS,
    TWITTER_DAILY_TWEET_FIELDS,
)
from ..ml.models.emotions_classification import *
from ..ml.models.intent_classification import *
from ..ml.models.keyword_analysis import *
from ..ml.models.ml_features import *
from ..ml.models.noteworthy_classification import *
from ..ml.models.preprocessing import *
from ..ml.models.sentiment_classification import *
from ..ml.models.thoughtful_classification import *
from ..ml.models.topic_matching import *
from .connect import db
from .status_check import check_status

# Load environment variables
load_dotenv()

# Constants
TWITTER_DAILY_DATA_PATH = os.getenv("TWITTER_DAILY_DATA_PATH")
TWITTER_DAILY_ETL_LOG_FILE = os.getenv("TWITTER_DAILY_ETL_LOG_FILE")
DB_TWIITER_TWEETS_COLLECTION = os.getenv("DB_TWIITER_TWEETS_COLLECTION")
DB_TWITTER_COMMENTS_COLLECTION = os.getenv("DB_TWITTER_COMMENTS_COLLECTION")
SG_TIMEZONE = pytz.timezone("Asia/Singapore")
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
latest_collection_date = datetime.strptime(status_jobj["twitter"]["latest_collection_date"], "%Y-%m-%d")
latest_etl_date = datetime.strptime(status_jobj["twitter"]["latest_etl_date"], "%Y-%m-%d")
curr_date = datetime.now(SG_TIMEZONE).date()

if (latest_collection_date.date() == curr_date) and (latest_etl_date.date() < latest_collection_date.date()):
    main_start = time.time()
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
        df = pd.read_json(
            f"{TWITTER_DAILY_DATA_PATH}/{latest_collection_date.date()}/{file}",
            orient="records",
            lines=True,
        )

        # Filtered unwanted data and data columns
        df_en = df[df["language"] == "en"]
        df_filtered = df_en[TWITTER_DAILY_TWEET_FIELDS]

        # Spilt data in tweets and comments
        df_tweets = df_filtered.loc[df_filtered["reply_to"].isin([[]])].reset_index()
        df_comments = df_filtered[df_filtered["reply_to"].isin([[]]) == False].reset_index()
        df_comments["parent_id"] = df_comments["reply_to"].apply(lambda x: int(x[0]["id"]))

        # Apply preprocessing on text to clean data
        df_tweets["cleantext"] = df_tweets["tweet"].apply(twitter_preprocessing)
        df_comments["cleantext"] = df_comments["tweet"].apply(twitter_preprocessing)

        ###########################################################
        #################### RUNNING ML MODELS ####################
        ###########################################################

        logger.info(f"Now classifying {file}\n")

        ###################  KEYWORD ANALYSIS ####################
        start1 = time()
        df_tweets["entities"] = df_tweets["cleantext"].apply(extract_entities)
        df_comments["entities"] = df_comments["cleantext"].apply(extract_entities)

        hours, mins, seconds = get_time(time() - start1)
        logger.info(f"KEYWORD ANALYSIS took: {hours} hours, {mins} mins, {seconds} seconds\n")

        ####################  EMOTIONS CLASSIFICATION ####################
        start = time()
        df_tweets["emotions_label"] = df_tweets["cleantext"].apply(lambda x: classify_emotions(x))
        df_comments["emotions_label"] = df_comments["cleantext"].apply(lambda x: classify_emotions(x))

        hours, mins, seconds = get_time(time() - start)
        logger.info(f"EMOTIONS CLASSIFICATION took: {hours} hours, {mins} mins, {seconds} seconds\n")

        #################### TOPIC CLASSIFICATION ####################
        start = time()
        df_tweets["topic"] = df_tweets["cleantext"].apply(get_topics)
        df_comments["topic"] = df_comments["cleantext"].apply(get_topics)

        hours, mins, seconds = get_time(time() - start)
        logger.info(f"TOPIC CLASSIFICATION took: {hours} hours, {mins} mins, {seconds} seconds\n")

        #################### INTENT CLASSIFICATION ####################
        start = time()
        df_tweets["intent"] = df_tweets["cleantext"].apply(classify_intent)
        df_comments["intent"] = df_comments["cleantext"].apply(classify_intent)

        hours, mins, seconds = get_time(time() - start)
        logger.info(f"INTENT CLASSIFICATION took: {hours} hours, {mins} mins, {seconds} seconds\n")

        #################### SENTIMENT CLASSIFICATION ####################
        start = time()
        df_tweets = classify_sentiment(df_tweets)
        df_comments = classify_sentiment(df_comments)

        hours, mins, seconds = get_time(time() - start)
        logger.info(f"SENTIMENT CLASSIFICATION took: {hours} hours, {mins} mins, {seconds} seconds\n")

        #################### THOUGHTFULNESS CLASSIFICATION ####################
        start = time()
        df_post_features = create_features(df_tweets)
        df_post_features_standardised = get_standardized_values(df_post_features)
        post_predictions = predict_thoughtfulness(df_post_features_standardised)
        df_tweets["isThoughtful"] = post_predictions

        df_comments_features = create_features(df_comments)
        df_comments_features_standardised = get_standardized_values(df_comments_features)
        df_comments_predictions = predict_thoughtfulness(df_comments_features_standardised)
        df_comments["isThoughtful"] = df_comments_predictions

        hours, mins, seconds = get_time(time() - start)
        logger.info(f"THOUGHTFUL CLASSIFICATION took: {hours} hours, {mins} mins, {seconds} seconds\n")

        #################### NOTEWORTHY CLASSIFICATION ####################
        start = time()
        df_tweets["isNoteworthy"] = df_tweets.apply(classify_noteworthy, axis=1)
        df_comments["isNoteworthy"] = df_comments.apply(classify_noteworthy, axis=1)

        hours, mins, seconds = get_time(time() - start)
        logger.info(f"NOTEWORTHY CLASSIFICATION took: {hours} hours, {mins} mins, {seconds} seconds\n")

        ##########################################################
        ############### END OF ML CLASSIFICATION #################
        ##########################################################

        # Convert df to dict format
        tweets = df_tweets.to_dict(orient="index")
        comments = df_comments.to_dict(orient="index")

        # Insert tweets and comments into their respective db collection
        twitter_tweets.insert_many([tweets[i] for i in range(len(tweets))])
        twitter_comments.insert_many([comments[i] for i in range(len(comments))])

        logger.info(f"{file} processed")

    # Update status file
    status_jobj["twitter"]["latest_etl_date"] = datetime.now().date().strftime("%Y-%m-%d")
    with open(STATUS_CHECK_FILE, "w") as f:
        json.dump(status_jobj, f, indent=4)

    duration = time.time() - main_start
    logger.info(f"Daily ETL for Twitter in GPU server completed, time taken: {duration}")
    tele.send(messages=[f"Daily ETL for Twitter in GPU server completed, time taken: {duration}"])
