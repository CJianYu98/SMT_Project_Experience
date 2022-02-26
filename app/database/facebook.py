import json
import os

import pandas as pd
from dotenv import load_dotenv
from loguru import logger

from ..ml.models.sentiment_analysis import *
from .connect import client

# Load environment variables
load_dotenv()

# Constants
FACEBOOK_HISTORICAL_DATA_PATH = os.getenv("FACEBOOK_HISTORICAL_DATA_PATH")
FACEBOOK_HISTORICAL_OUTPUT_DATA_PATH = os.getenv("FACEBOOK_HISTORICAL_OUTPUT_DATA_PATH")

# Select MongoDB collection to work with
fb_posts = client.smt483.fb_posts
fb_comments = client.smt483.fb_comments

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
    df_new["fb_group"] = file_name

    # Filter df to df_posts and df_comments
    df_posts = df_new[df_new["is_post"] == 1]
    df_posts.reset_index(inplace=True, drop=True)
    df_comments = df_new[df_new["is_post"] == 0]
    df_comments.reset_index(inplace=True, drop=True)

    # Run classification on df_posts and df_comments
    df_posts["sentiment_label"] = df_posts["message"].apply(lambda x: classify_sentiment(x))
    df_posts["emotions_label"] = df_posts["message"].apply(lambda x: classify_emotions(x))
    df_comments["sentiment_label"] = df_comments["message"].apply(lambda x: classify_sentiment(x))
    df_comments["emotions_label"] = df_comments["message"].apply(lambda x: classify_emotions(x))

    # Save processed data to json file, with each row as a json record
    df_posts.to_json(f"{FACEBOOK_HISTORICAL_OUTPUT_DATA_PATH}/{file_name}_posts.json", orient="index")
    df_comments.to_json(f"{FACEBOOK_HISTORICAL_OUTPUT_DATA_PATH}/{file_name}_comments.json", orient="index")

    # Read the json date file
    posts = open(f"{FACEBOOK_HISTORICAL_OUTPUT_DATA_PATH}/{file_name}_posts.json")
    posts_data = json.load(posts)
    comments = open(f"{FACEBOOK_HISTORICAL_OUTPUT_DATA_PATH}/{file_name}_comments.json")
    comments_data = json.load(comments)

    # Insert data into MongoDB
    num_posts = len(posts_data)
    num_comments = len(comments_data)
    fb_posts.insert_many([posts_data[str(i)] for i in range(num_posts)])
    fb_comments.insert_many([comments_data[str(i)] for i in range(num_comments)])
