import json
import os
from datetime import datetime
from time import time

import pandas as pd
from dotenv import load_dotenv
from loguru import logger
from tqdm.auto import tqdm

from ..constants.etl import FACEBOOK_FIELDS, FACEBOOK_RENAME_COL_DICT, get_time
from ..constants.social_media import FACEBOOK_GROUPS
from ..ml.models.emotions_classification import *
from ..ml.models.intent_classification import *
from ..ml.models.keyword_analysis import *
from ..ml.models.ml_features import *
from ..ml.models.noteworthy_classification import *
from ..ml.models.preprocessing import *
from ..ml.models.sentiment_classification import *
from ..ml.models.thoughtful_classification import *
from ..ml.models.topic_classification import *
from .connect import client

pd.options.mode.chained_assignment = None  # to hide warning error
# tqdm.pandas()  # Enable progress bar for dataframe .apply using progress_apply

# Load constants
load_dotenv()
FACEBOOK_HISTORICAL_DATA_PATH = os.getenv("FACEBOOK_HISTORICAL_DATA_PATH")
FACEBOOK_HISTORICAL_OUTPUT_DATA_PATH = os.getenv("FACEBOOK_HISTORICAL_OUTPUT_DATA_PATH")

# Select MongoDB collection to work with
fb_posts = client.smt483.fb_posts
fb_comments = client.smt483.fb_comments

start_main = time()
for file in os.listdir(FACEBOOK_HISTORICAL_DATA_PATH):
    file_name = file[:-4]

    # Read data files
    df = pd.read_csv(f"{FACEBOOK_HISTORICAL_DATA_PATH}/{file}", header=1, low_memory=False)

    # Drop rows with error or missing data
    df.drop(df[df["query_status"] == "error (400)"].index, inplace=True)
    df.drop(df[df["object_type"] != "data"].index, inplace=True)
    df.dropna(subset=["created_time", "message"], inplace=True)

    # Filtered data with relevant columns
    df_new = df[FACEBOOK_FIELDS]

    # Rename columns
    df_new.rename(
        columns=FACEBOOK_RENAME_COL_DICT,
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

    # Apply preprocessing on text to clean data
    df_posts["cleantext"] = df_posts["message"].apply(preprocessing)
    df_comments["cleantext"] = df_comments["message"].apply(preprocessing)

    ###########################################################
    #################### RUNNING ML MODELS ####################
    ###########################################################

    logger.info(f"Now classifying {file_name}\n")

    ###################  KEYWORD ANALYSIS ####################
    start1 = time()
    df_posts["entities"] = df_posts["cleantext"].apply(extract_entities)
    df_comments["entities"] = df_comments["cleantext"].apply(extract_entities)

    hours, mins, seconds = get_time(time() - start1)
    logger.info(f"KEYWORD ANALYSIS took: {hours} hours, {mins} mins, {seconds} seconds\n")

    ####################  EMOTIONS CLASSIFICATION ####################
    start = time()
    df_posts["emotions_label"] = df_posts["message"].apply(lambda x: classify_emotions(x))
    df_comments["emotions_label"] = df_comments["message"].apply(lambda x: classify_emotions(x))

    hours, mins, seconds = get_time(time() - start)
    logger.info(f"EMOTIONS CLASSIFICATION took: {hours} hours, {mins} mins, {seconds} seconds\n")

    #################### TOPIC CLASSIFICATION ####################
    start = time()
    df_posts["topic"] = df_posts["cleantext"].apply(classify_topics)
    df_comments["topic"] = df_comments["cleantext"].apply(classify_topics)

    hours, mins, seconds = get_time(time() - start)
    logger.info(f"TOPIC CLASSIFICATION took: {hours} hours, {mins} mins, {seconds} seconds\n")

    #################### INTENT CLASSIFICATION ####################
    start = time()
    df_posts["intent"] = df_posts["cleantext"].apply(classify_intent)
    df_comments["intent"] = df_comments["cleantext"].apply(classify_intent)

    hours, mins, seconds = get_time(time() - start)
    logger.info(f"INTENT CLASSIFICATION took: {hours} hours, {mins} mins, {seconds} seconds\n")

    #################### SENTIMENT CLASSIFICATION ####################
    start = time()
    df_posts = classify_sentiment(df_posts)
    df_comments = classify_sentiment(df_comments)

    hours, mins, seconds = get_time(time() - start)
    logger.info(f"SENTIMENT CLASSIFICATION took: {hours} hours, {mins} mins, {seconds} seconds\n")

    #################### THOUGHTFULNESS CLASSIFICATION ####################
    start = time()
    df_post_features = create_features(df_posts)
    df_post_features_standardised = get_standardized_values(df_post_features)
    post_predictions = predict_thoughtfulness(df_post_features_standardised)
    df_posts["isThoughtful"] = post_predictions

    df_comments_features = create_features(df_comments)
    df_comments_features_standardised = get_standardized_values(df_comments_features)
    df_comments_predictions = predict_thoughtfulness(df_comments_features_standardised)
    df_comments["isThoughtful"] = df_comments_predictions

    hours, mins, seconds = get_time(time() - start)
    logger.info(f"THOUGHTFUL CLASSIFICATION took: {hours} hours, {mins} mins, {seconds} seconds\n")

    #################### NOTEWORTHY CLASSIFICATION ####################
    start = time()
    df_posts["isNoteworthy"] = df_posts.apply(classify_noteworthy, axis=1)
    df_comments["isNoteworthy"] = df_comments.apply(classify_noteworthy, axis=1)

    hours, mins, seconds = get_time(time() - start)
    logger.info(f"NOTEWORTHY CLASSIFICATION took: {hours} hours, {mins} mins, {seconds} seconds\n")

    ##########################################################
    ############### END OF ML CLASSIFICATION #################
    ##########################################################

    # Convert dataframe to dict
    posts = df_posts.to_dict(orient="index")
    comments = df_comments.to_dict(orient="index")

    # Insert data into MongoDB
    num_posts = len(posts)
    num_comments = len(comments)
    fb_posts.insert_many([posts[i] for i in range(num_posts)])
    fb_comments.insert_many([comments[i] for i in range(num_comments)])

    hours, mins, seconds = get_time(time() - start1)
    logger.info(f">>>> {file_name} done.\n{file_name} took {hours} hours, {mins} mins, {seconds} seconds in total.")

hours, mins, seconds = get_time(time() - start_main)
print("################# FB ML Classification Complete #################")
print(f"Total time taken is {hours} hours, {mins} mins, {seconds} seconds.")
