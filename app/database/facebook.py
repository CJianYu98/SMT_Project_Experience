import json
import os
import time
from datetime import datetime

import pandas as pd
from dotenv import load_dotenv
from loguru import logger

from ..constants.social_media import FACEBOOK_GROUPS
from ..ml.models.preprocessing import *
from ..ml.models.keyword_analysis import *
from ..ml.models.sentiment_analysis import *
from ..ml.models.intent_classification import *
from .connect import client

# Load environment variables
load_dotenv()

# Constants
FACEBOOK_HISTORICAL_DATA_PATH = os.getenv("FACEBOOK_HISTORICAL_DATA_PATH")
FACEBOOK_HISTORICAL_OUTPUT_DATA_PATH = os.getenv("FACEBOOK_HISTORICAL_OUTPUT_DATA_PATH")

# Select MongoDB collection to work with
fb_posts = client.smt483.fb_posts_test
fb_comments = client.smt483.fb_comments_test

for file in os.listdir(FACEBOOK_HISTORICAL_DATA_PATH):
    file_name = file[:-4]

    # Read data files
    df = pd.read_csv(f"{FACEBOOK_HISTORICAL_DATA_PATH}/{file}", header=1)

    # Drop rows with error or missing data
    df.drop(df[df["query_status"] == "error (400)"].index, inplace=True)
    df.drop(df[df["object_type"] != "data"].index, inplace=True)
    df.dropna(subset=["created_time", "message"], inplace=True)

    # Set relevant columns
    facebook_fields = [
        "id",
        "query_type",
        "parent_id",
        "object_id",
        "message",
        "created_time",
        "comments.summary.total_count",
        "reactions.summary.total_count",
        "like.summary.total_count",
        "love.summary.total_count",
        "haha.summary.total_count",
        "wow.summary.total_count",
        "sad.summary.total_count",
        "angry.summary.total_count",
    ]

    # Filtered data with relevant columns
    df_new = df[facebook_fields]

    # Rename columns
    df_new.rename(
        columns={
            "query_type": "is_post",
            "comments.summary.total_count": "comments_cnt",
            "reactions.summary.total_count": "reactions_cnt",
            "like.summary.total_count": "likes_cnt",
            "love.summary.total_count": "loves_cnt",
            "haha.summary.total_count": "haha_cnt",
            "wow.summary.total_count": "wow_cnt",
            "sad.summary.total_count": "sad_cnt",
            "angry.summary.total_count": "angry_cnt",
        },
        inplace=True,
    )

    # Label encoding
    df_new["is_post"].replace({"Facebook:/<page-id>/posts": 1, "Facebook:/<post-id>/comments": 0}, inplace=True)

    # Add fb_group column
    df_new["fb_group"] = FACEBOOK_GROUPS[file_name]

    # Convert data type
    df_new["created_time"] = df_new["created_time"].apply(lambda x: datetime.strptime(x, "%Y-%m-%dT%H:%M:%S%z"))
    df_new["parent_id"] = df_new["parent_id"].apply(lambda x: int(x))

    # Filter df to df_posts and df_comments
    df_posts = df_new[df_new["is_post"] == 1].drop(["is_post"], axis=1)
    df_posts.reset_index(inplace=True, drop=True)
    df_comments = df_new[df_new["is_post"] == 0].drop(["is_post"], axis=1)
    df_comments.reset_index(inplace=True, drop=True)

    #Apply preprocessing on text to clean data
    df_posts["cleantext"] = df_posts["message"].apply(preprocessing)
    # df_comments["cleantext"] = df_comments["message"].apply(preprocessing)

    # Classify Sentiment on df_posts and df_comments
    logger.info(f"Now classifying {file_name}")
    start = time.process_time()
    df_posts = classify_sentiment(df_posts)
    # df_comments = classify_sentiment(df_comments)
    print("Sentiment classification took: ", time.process_time() - start)

    # Classify Emotions on df_posts and df_comments
    # df_posts["emotions_label"] = df_posts["message"].apply(lambda x: classify_emotions(x))
    # df_comments["emotions_label"] = df_comments["message"].apply(lambda x: classify_emotions(x))

    # Extract entities from df_posts and df_comments
    start2 = time.process_time()
    df_posts["entities"] = df_posts["cleantext"].apply(extract_entities)
    # df_comments["entities"] = df_posts["cleantext"].apply(extract_entities)
    print("NER took: ", time.process_time() - start2)

    # Classify Intention on df_posts and df_comments
    df_posts["intent"] = df_posts["cleantext"].apply(classify_intent)

    # Convert dataframe to dict
    posts = df_posts.to_dict(orient="index")
    comments = df_comments.to_dict(orient="index")

    # Insert data into MongoDB
    num_posts = len(posts)
    num_comments = len(comments)
    fb_posts.insert_many([posts[i] for i in range(num_posts)])
    fb_comments.insert_many([comments[i] for i in range(num_comments)])