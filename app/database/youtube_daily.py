import json
import os
import uuid
from datetime import datetime, timedelta
from pprint import pprint
from time import time

import pandas as pd
import pytz
from dotenv import load_dotenv
from loguru import logger

from ..constants.etl import get_time
from ..constants.social_media import YOUTUBE_COMMENT_FIELDS, YOUTUBE_VIDEO_FIELDS
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

pd.options.mode.chained_assignment = None  # to hide warning error

# Load environment variables
load_dotenv()

# Constants
YOUTUBE_DAILY_DATA_PATH = os.getenv("YOUTUBE_DAILY_DATA_PATH")
YOUTUBE_DAILY_ETL_LOG_FILE = os.getenv("YOUTUBE_DAILY_ETL_LOG_FILE")
DB_YOUTUBE_VIDEOS_COLLECTION = os.getenv("DB_YOUTUBE_VIDEOS_COLLECTION")
DB_YOUTUBE_COMMENTS_COLLECTION = os.getenv("DB_YOUTUBE_COMMENTS_COLLECTION")

# Add logger configurations
logger.add(
    YOUTUBE_DAILY_ETL_LOG_FILE,
    format="{time} {file} {level} {message}",
    level="DEBUG",
)

# Select MongoDB collection to work with
youtube_videos = db[DB_YOUTUBE_VIDEOS_COLLECTION]
youtube_comments = db[DB_YOUTUBE_COMMENTS_COLLECTION]

# Func for cleaning data columns
def date_str_to_dt(date: str) -> datetime:
    global crawled_date_str
    if "ago" in date:
        return datetime.strptime(crawled_date_str, "%Y-%m-%d")
    elif "Premiered" in date or "Premieres" in date:
        return datetime.strptime(date[10:], "%b %d, %Y")
    elif "Streamed" in date:
        return datetime.strptime(date[17:], "%b %d, %Y")
    else:
        return datetime.strptime(date, "%b %d, %Y")


def likes_str_to_int(likes: str) -> int:
    if likes == "LIKE":
        return 0
    elif "K" in likes or "k" in likes:
        return int(float(likes[:-1]) * 1000)
    else:
        return int(likes)


def views_str_to_int(views: str) -> int:
    if "waiting" in views:
        return 0
    else:
        return int(views[:-6].replace(",", ""))


files = sorted(os.listdir(YOUTUBE_DAILY_DATA_PATH))
for file in files:
    logger.info(f"Starting to ETL Youtube {file}")

    # Store all the comments
    comments = []

    # Retrieve all youtube video ids and delete all videos within date range
    crawled_date_str = file[:-5]
    end_date = datetime.strptime(crawled_date_str, "%Y-%m-%d")
    start_date = end_date - timedelta(days=13)
    db_query = {"date_uploaded": {"$gte": start_date, "$lte": end_date}}
    videos = list(youtube_videos.find(db_query))
    vid_ids = [vid["id"] for vid in videos]
    youtube_videos.delete_many(db_query)

    for v_id in vid_ids:
        youtube_comments.delete_many({"vid_id": v_id})

    with open(f"{YOUTUBE_DAILY_DATA_PATH}/{file}") as f:
        jobj = json.load(f)
        for channel, data in jobj.items():
            if data:
                df = pd.DataFrame(data)
                col_names = {col: col.lower() for col in df.columns}
                col_names["Date Uploaded"] = "date_uploaded"
                df.rename(columns=col_names, inplace=True)

                df["date_uploaded"] = df["date_uploaded"].apply(date_str_to_dt)
                df["id"] = df.apply(lambda x: uuid.uuid4().hex, axis=1)
                df["channel"] = channel
                df["views"] = df["views"].apply(views_str_to_int)
                df["likes"] = df["likes"].apply(likes_str_to_int)

                df_videos = df.drop("comments", axis=1)
                df_videos["combined_text"] = df["title"] + " " + df["description"]

                df_exploded = df.explode("comments").reset_index(drop=True)
                df_exploded["cid"] = df_exploded.apply(lambda x: uuid.uuid4().hex, axis=1)
                df_comments = df_exploded[["cid", "id", "comments"]]
                df_comments.rename(columns={"id": "vid_id", "cid": "id", "comments": "comment"}, inplace=True)

                # Apply preprocessing on text to clean data
                df_videos["cleantext"] = df_videos["combined_text"].apply(preprocessing)
                df_comments["cleantext"] = df_comments["comment"].apply(preprocessing)

                ###########################################################
                #################### RUNNING ML MODELS ####################
                ###########################################################

                logger.info(f"Now classifying {channel}\n")

                ###################  KEYWORD ANALYSIS ####################
                start1 = time()
                df_videos["entities"] = df_videos["cleantext"].apply(extract_entities)
                df_comments["entities"] = df_comments["cleantext"].apply(extract_entities)

                hours, mins, seconds = get_time(time() - start1)
                logger.info(f"KEYWORD ANALYSIS took: {hours} hours, {mins} mins, {seconds} seconds\n")

                ####################  EMOTIONS CLASSIFICATION ####################
                start = time()
                df_videos["emotions_label"] = df_videos["cleantext"].apply(lambda x: classify_emotions(x))
                df_comments["emotions_label"] = df_comments["cleantext"].apply(lambda x: classify_emotions(x))

                hours, mins, seconds = get_time(time() - start)
                logger.info(f"EMOTIONS CLASSIFICATION took: {hours} hours, {mins} mins, {seconds} seconds\n")

                #################### TOPIC CLASSIFICATION ####################
                start = time()
                df_videos["topic"] = df_videos["cleantext"].apply(get_topics)
                df_comments["topic"] = df_comments["cleantext"].apply(get_topics)

                hours, mins, seconds = get_time(time() - start)
                logger.info(f"TOPIC CLASSIFICATION took: {hours} hours, {mins} mins, {seconds} seconds\n")

                #################### INTENT CLASSIFICATION ####################
                start = time()
                df_videos["intent"] = df_videos["cleantext"].apply(classify_intent)
                df_comments["intent"] = df_comments["cleantext"].apply(classify_intent)

                hours, mins, seconds = get_time(time() - start)
                logger.info(f"INTENT CLASSIFICATION took: {hours} hours, {mins} mins, {seconds} seconds\n")

                #################### SENTIMENT CLASSIFICATION ####################
                start = time()
                df_videos = classify_sentiment(df_videos)
                df_comments = classify_sentiment(df_comments)

                hours, mins, seconds = get_time(time() - start)
                logger.info(f"SENTIMENT CLASSIFICATION took: {hours} hours, {mins} mins, {seconds} seconds\n")

                #################### THOUGHTFULNESS CLASSIFICATION ####################
                start = time()
                df_post_features = create_features(df_videos)
                df_post_features_standardised = get_standardized_values(df_post_features)
                post_predictions = predict_thoughtfulness(df_post_features_standardised)
                df_videos["isThoughtful"] = post_predictions

                df_comments_features = create_features(df_comments)
                df_comments_features_standardised = get_standardized_values(df_comments_features)
                df_comments_predictions = predict_thoughtfulness(df_comments_features_standardised)
                df_comments["isThoughtful"] = df_comments_predictions

                hours, mins, seconds = get_time(time() - start)
                logger.info(f"THOUGHTFUL CLASSIFICATION took: {hours} hours, {mins} mins, {seconds} seconds\n")

                #################### NOTEWORTHY CLASSIFICATION ####################
                start = time()
                df_videos["isNoteworthy"] = df_videos.apply(classify_noteworthy, axis=1)
                df_comments["isNoteworthy"] = df_comments.apply(classify_noteworthy, axis=1)

                hours, mins, seconds = get_time(time() - start)
                logger.info(f"NOTEWORTHY CLASSIFICATION took: {hours} hours, {mins} mins, {seconds} seconds\n")

                ##########################################################
                ############### END OF ML CLASSIFICATION #################
                ##########################################################

                yt_vid_data = df_videos.to_dict(orient="index")
                yt_comments_data = df_comments.to_dict(orient="index")

                youtube_videos.insert_many([yt_vid_data[i] for i in range(len(yt_vid_data))])
                youtube_comments.insert_many([yt_comments_data[i] for i in range(len(yt_comments_data))])
