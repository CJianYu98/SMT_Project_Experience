import json
import os
from time import time
from datetime import datetime, timedelta
from pprint import pprint

import pandas as pd
import pytz
import telegram_send as tele
from dotenv import load_dotenv
from loguru import logger

from ..constants.etl import get_time
from ..constants.social_media import (
    REDDIT_DAILY_COMMENT_FIELDS,
    REDDIT_DAILY_SUBMISSION_FIELDS
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
from .connect import client
from .connect import db

pd.options.mode.chained_assignment = None  # to hide warning error

# Load environment variables
load_dotenv()

# Constants
REDDIT_DAILY_DATA_PATH = os.getenv("REDDIT_DAILY_DATA_PATH")
REDDIT_DAILY_ETL_LOG_FILE = os.getenv("REDDIT_DAILY_ETL_LOG_FILE")
DB_REDDIT_SUBMISSIONS_COLLECTION = os.getenv("DB_REDDIT_SUBMISSIONS_COLLECTION")
DB_REDDIT_COMMENTS_COLLECTION = os.getenv("DB_REDDIT_COMMENTS_COLLECTION")

# Add logger configurations
logger.add(
    REDDIT_DAILY_ETL_LOG_FILE,
    format="{time} {file} {level} {message}",
    level="DEBUG",
)

# Select MongoDB collection to work with
reddit_submissions = db[DB_REDDIT_SUBMISSIONS_COLLECTION]
reddit_comments = db[DB_REDDIT_COMMENTS_COLLECTION]

files = sorted(os.listdir(REDDIT_DAILY_DATA_PATH))
for i, file in enumerate(files):
    start = time()
    logger.info(f"Starting to ETL Reddit {file}")
    # tele.send(messages=[f"Starting to ETL Reddit {file}"])

    # Delete all submissions within date range
    date = file[:-5]
    end_date = datetime.strptime(date, "%Y-%m-%d")
    start_date = end_date - timedelta(days=14)
    db_query = {"created_datetime": {"$gte": start_date, "$lte": end_date}}
    subs = list(reddit_submissions.find(db_query))
    sub_ids = [sub["id"] for sub in subs]
    reddit_submissions.delete_many(db_query)

    # Read in json date file for each date
    df = pd.read_json(f"{REDDIT_DAILY_DATA_PATH}/{file}", orient="index")

    # Process data for Reddit submissions
    df_sub = df[REDDIT_DAILY_SUBMISSION_FIELDS]
    df_sub.reset_index(drop=True, inplace=True)
    df_sub.rename(columns={"created_utc": "created_datetime"}, inplace=True)
    df_sub["created_datetime"] = df_sub["created_datetime"].apply(
        lambda x: datetime.fromtimestamp(x).astimezone(pytz.UTC)
    )

    # Delete all comments under a submission, then bulk insert all comments instead (faster time performance)
    for sub_id in sub_ids:
        reddit_comments.delete_many({"submission_id": sub_id})

    # Process data for Reddit comments
    comments = []
    for i in range(len(df)):
        if df.iloc[i]["comments"]:
            for cid, c_data in df.iloc[i]["comments"].items():
                comment = {}
                for field in REDDIT_DAILY_COMMENT_FIELDS:
                    try:
                        if field == "created_utc":
                            dt = datetime.fromtimestamp(c_data[field]).astimezone(pytz.UTC)
                            comment["created_datetime"] = dt
                        elif field == "_submission":
                            comment["submission_id"] = c_data[field]
                        elif field == "parent_id":
                            pid = c_data[field].split("_")[1]
                            comment["parent_id"] = pid
                        else:
                            comment[field] = c_data[field]
                    except:
                        continue
                comments.append(comment)
    
    # Create DataFrame to store comments
    df_comments = pd.DataFrame(comments)

    # Split posts into separate DataFrames for records that do not have text body
    df_empty_text = df_sub[df_sub["selftext"] == "[removed]"]
    df_with_text = df_sub[df_sub["selftext"] != "[removed]"]
    df_with_text["combined_text"] = df_with_text["title"] + " " + df_with_text["selftext"] # Combine post title and text body for modelling

    # Apply preprocessing on text to clean data
    df_with_text["cleantext"] = df_with_text["combined_text"].apply(preprocessing)
    df_comments["cleantext"] = df_comments["body"].apply(preprocessing)

    ###########################################################
    #################### RUNNING ML MODELS ####################
    ###########################################################

    logger.info(f"Now classifying {file}\n")

    ###################  KEYWORD ANALYSIS ####################
    start1 = time()
    df_with_text["entities"] = df_with_text["cleantext"].apply(extract_entities)
    df_comments["entities"] = df_comments["cleantext"].apply(extract_entities)

    hours, mins, seconds = get_time(time() - start1)
    logger.info(f"KEYWORD ANALYSIS took: {hours} hours, {mins} mins, {seconds} seconds\n")

    ####################  EMOTIONS CLASSIFICATION ####################
    start = time()
    df_with_text["emotions_label"] = df_with_text["cleantext"].apply(lambda x: classify_emotions(x))
    df_comments["emotions_label"] = df_comments["cleantext"].apply(lambda x: classify_emotions(x))
    hours, mins, seconds = get_time(time() - start)
    logger.info(f"EMOTIONS CLASSIFICATION took: {hours} hours, {mins} mins, {seconds} seconds\n")

    #################### TOPIC CLASSIFICATION ####################
    start = time()

    df_with_text["topic"] = df_with_text["cleantext"].apply(get_topics)
    df_comments["topic"] = df_comments["cleantext"].apply(get_topics)

    hours, mins, seconds = get_time(time() - start)
    logger.info(f"TOPIC CLASSIFICATION took: {hours} hours, {mins} mins, {seconds} seconds\n")

    #################### INTENT CLASSIFICATION ####################
    start = time()
    df_with_text["intent"] = df_with_text["cleantext"].apply(classify_intent)
    df_comments["intent"] = df_comments["cleantext"].apply(classify_intent)

    hours, mins, seconds = get_time(time() - start)
    logger.info(f"INTENT CLASSIFICATION took: {hours} hours, {mins} mins, {seconds} seconds\n")

    #################### SENTIMENT CLASSIFICATION ####################
    start = time()
    df_with_text = classify_sentiment(df_with_text)
    df_comments = classify_sentiment(df_comments)

    hours, mins, seconds = get_time(time() - start)
    logger.info(f"SENTIMENT CLASSIFICATION took: {hours} hours, {mins} mins, {seconds} seconds\n")

    #################### THOUGHTFULNESS CLASSIFICATION ####################
    start = time()
    df_with_text_features = create_features(df_with_text)
    df_features_standardised = get_standardized_values(df_with_text_features)
    post_predictions = predict_thoughtfulness(df_features_standardised)
    df_with_text["isThoughtful"] = post_predictions

    df_comments_features = create_features(df_comments)
    df_comments_features_standardised = get_standardized_values(df_comments_features)
    comments_predictions = predict_thoughtfulness(df_comments_features_standardised)
    df_comments["isThoughtful"] = comments_predictions

    hours, mins, seconds = get_time(time() - start)
    logger.info(f"THOUGHTFUL CLASSIFICATION took: {hours} hours, {mins} mins, {seconds} seconds\n")

    #################### NOTEWORTHY CLASSIFICATION ####################
    start = time()
    df_with_text["isNoteworthy"] = df_with_text.apply(classify_noteworthy, axis=1)
    df_comments["isNoteworthy"] = df_comments.apply(classify_noteworthy, axis=1)

    hours, mins, seconds = get_time(time() - start)
    logger.info(f"NOTEWORTHY CLASSIFICATION took: {hours} hours, {mins} mins, {seconds} seconds\n")

    #########################################################
    ############## END OF ML CLASSIFICATION #################
    #########################################################

    # Merging back all the posts to a single dataframe 
    df_sub = pd.concat([df_with_text, df_empty_text])

    sub_data = df_sub.to_dict("index")
    comments_data = df_comments.to_dict("index")

    # TESTING WIP
    # print("Posts:\n")
    # print(df_sub.columns)
    # print(df_sub.head())
    # print(df_sub.tail())
    # print(sub_data)

    # print("Comments:\n")
    # print(df_comments.columns)
    # print(df_comments.iloc[:5])
    # print(df_comments.tail())
    # print(comments_data)

    reddit_submissions.insert_many(sub_data[i] for i in range(len(sub_data)))    
    reddit_comments.insert_many(comments_data)

    logger.info(f"Num submissions: {len(sub_data)}, Num comments: {len(comments_data)}")

    duration = time.time() - start
    logger.info(f"ETL Reddit {file} took {duration}")
    tele.send(messages=[f"ETL Reddit {file} took {duration}"])
    
