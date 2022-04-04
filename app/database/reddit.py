import json
import os
from time import time
from datetime import datetime, timedelta
from pprint import pprint

import pytz
from dotenv import load_dotenv
from loguru import logger

from ..constants.etl import get_time
from ..constants.social_media import (
    REDDIT_COMMENT_FIELDS,
    REDDIT_SUBMISSION_FIELDS
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
REDDIT_HISTORICAL_DATA_PATH = os.getenv("REDDIT_HISTORICAL_DATA_PATH")
DB_REDDIT_SUBMISSIONS_COLLECTION = os.getenv("DB_REDDIT_SUBMISSIONS_COLLECTION")
DB_REDDIT_COMMENTS_COLLECTION = os.getenv("DB_REDDIT_COMMENTS_COLLECTION")

# Select MongoDB collection to work with
reddit_submissions = db[DB_REDDIT_SUBMISSIONS_COLLECTION]
reddit_comments = db[DB_REDDIT_COMMENTS_COLLECTION]

for year_folder in os.listdir(REDDIT_HISTORICAL_DATA_PATH):
    if year_folder in (".DS_Store", "2022"):
        continue
    # Inserting reddit submissions data
    for sid_file in os.listdir(f"{REDDIT_HISTORICAL_DATA_PATH}/{year_folder}/sids"):
        if sid_file == ".DS_Store":
            continue

        logger.info(f"Inserting submissions data for {sid_file} in {year_folder} folder")

        submission_data = []

        with open(f"{REDDIT_HISTORICAL_DATA_PATH}/{year_folder}/sids/{sid_file}") as f:
            for line in f:
                jobj = json.loads(line)

                sub = {}
                for field in REDDIT_SUBMISSION_FIELDS:
                    try:
                        if field == "created_utc":
                            dt = datetime.fromtimestamp(jobj[field]).astimezone(pytz.UTC)
                            sub["created_datetime"] = dt
                        else:
                            sub[field] = jobj[field]
                    except:
                        continue
                submission_data.append(sub)

        # Create DataFrame to store submissions
        df_sub = pd.DataFrame(submission_data)

        # Split posts into separate DataFrames for records that do not have text body
        df_empty_text = df_sub[df_sub["selftext"] == "[removed]"]
        df_with_text = df_sub[df_sub["selftext"] != "[removed]"]
        df_with_text["combined_text"] = df_with_text["title"] + " " + df_with_text["selftext"] # Combine post title and text body for modelling

        # Apply preprocessing on text to clean data
        df_with_text["cleantext"] = df_with_text["combined_text"].apply(preprocessing)

        ###########################################################
        #################### RUNNING ML MODELS ####################
        ###########################################################

        logger.info(f"Now classifying {sid_file}\n")

        ###################  KEYWORD ANALYSIS ####################
        start1 = time()
        df_with_text["entities"] = df_with_text["cleantext"].apply(extract_entities)

        hours, mins, seconds = get_time(time() - start1)
        logger.info(f"KEYWORD ANALYSIS took: {hours} hours, {mins} mins, {seconds} seconds\n")

        ####################  EMOTIONS CLASSIFICATION ####################
        start = time()
        df_with_text["emotions_label"] = df_with_text["cleantext"].apply(lambda x: classify_emotions(x))
        
        hours, mins, seconds = get_time(time() - start)
        logger.info(f"EMOTIONS CLASSIFICATION took: {hours} hours, {mins} mins, {seconds} seconds\n")

        #################### TOPIC CLASSIFICATION ####################
        start = time()

        df_with_text["topic"] = df_with_text["cleantext"].apply(get_topics)

        hours, mins, seconds = get_time(time() - start)
        logger.info(f"TOPIC CLASSIFICATION took: {hours} hours, {mins} mins, {seconds} seconds\n")

        #################### INTENT CLASSIFICATION ####################
        start = time()
        df_with_text["intent"] = df_with_text["cleantext"].apply(classify_intent)

        hours, mins, seconds = get_time(time() - start)
        logger.info(f"INTENT CLASSIFICATION took: {hours} hours, {mins} mins, {seconds} seconds\n")

        #################### SENTIMENT CLASSIFICATION ####################
        start = time()
        df_with_text = classify_sentiment(df_with_text)

        hours, mins, seconds = get_time(time() - start)
        logger.info(f"SENTIMENT CLASSIFICATION took: {hours} hours, {mins} mins, {seconds} seconds\n")

        #################### THOUGHTFULNESS CLASSIFICATION ####################
        start = time()
        df_with_text_features = create_features(df_with_text)
        df_features_standardised = get_standardized_values(df_with_text_features)
        post_predictions = predict_thoughtfulness(df_features_standardised)
        df_with_text["isThoughtful"] = post_predictions

        hours, mins, seconds = get_time(time() - start)
        logger.info(f"THOUGHTFUL CLASSIFICATION took: {hours} hours, {mins} mins, {seconds} seconds\n")

        #################### NOTEWORTHY CLASSIFICATION ####################
        start = time()
        df_with_text["isNoteworthy"] = df_with_text.apply(classify_noteworthy, axis=1)

        hours, mins, seconds = get_time(time() - start)
        logger.info(f"NOTEWORTHY CLASSIFICATION took: {hours} hours, {mins} mins, {seconds} seconds\n")

        #########################################################
        ############## END OF ML CLASSIFICATION #################
        #########################################################

        # Merging back all the posts to a single dataframe 
        df_sub = pd.concat([df_with_text, df_empty_text])

        sub_data = df_sub.to_dict("index")
        reddit_submissions.insert_many(sub_data[i] for i in range(len(sub_data)))

    # Inserting reddit comments data
    for comment_file in os.listdir(f"{REDDIT_HISTORICAL_DATA_PATH}/{year_folder}/comments"):
        if comment_file == ".DS_Store":
            continue

        logger.info(f"Inserting comments data for {comment_file} in {year_folder} folder")

        with open(f"{REDDIT_HISTORICAL_DATA_PATH}/{year_folder}/comments/{comment_file}") as f:
            lines = f.readlines()

        comments_data = []

        for i in range(len(lines)):
            record = lines[i].split("\t")[2]
            comments = json.loads(record)["data"]

            for j in range(len(comments)):
                cmt = {}
                for field in REDDIT_COMMENT_FIELDS:
                    try:
                        if field == "created_utc":
                            dt = datetime.fromtimestamp(comments[j][field]).astimezone(pytz.UTC)
                            cmt["created_datetime"] = dt
                        elif field == "parent_id":
                            pid = comments[j][field].split('_')[1]
                            cmt["parent_id"] = pid
                        elif field == "link_id":
                            sub_id = comments[j][field].split('_')[1]
                            cmt['submission_id'] = sub_id
                        else:
                            cmt[field] = comments[j][field]
                    except:
                        continue
                comments_data.append(cmt)
        
        # Create DataFrame to store comments
        df_comments = pd.DataFrame(comments_data)

        # Apply preprocessing on text to clean data
        df_comments["cleantext"] = df_comments["body"].apply(preprocessing)

        ###########################################################
        #################### RUNNING ML MODELS ####################
        ###########################################################

        logger.info(f"Now classifying {comment_file}\n")

        ###################  KEYWORD ANALYSIS ####################
        start1 = time()
        df_comments["entities"] = df_comments["cleantext"].apply(extract_entities)
        hours, mins, seconds = get_time(time() - start1)
        logger.info(f"KEYWORD ANALYSIS took: {hours} hours, {mins} mins, {seconds} seconds\n")

        ####################  EMOTIONS CLASSIFICATION ####################
        start = time()
        df_comments["emotions_label"] = df_comments["cleantext"].apply(lambda x: classify_emotions(x))
        hours, mins, seconds = get_time(time() - start)
        logger.info(f"EMOTIONS CLASSIFICATION took: {hours} hours, {mins} mins, {seconds} seconds\n")

        #################### TOPIC CLASSIFICATION ####################
        start = time()
        df_comments["topic"] = df_comments["cleantext"].apply(get_topics)

        hours, mins, seconds = get_time(time() - start)
        logger.info(f"TOPIC CLASSIFICATION took: {hours} hours, {mins} mins, {seconds} seconds\n")

        #################### INTENT CLASSIFICATION ####################
        start = time()
        df_comments["intent"] = df_comments["cleantext"].apply(classify_intent)

        hours, mins, seconds = get_time(time() - start)
        logger.info(f"INTENT CLASSIFICATION took: {hours} hours, {mins} mins, {seconds} seconds\n")

        #################### SENTIMENT CLASSIFICATION ####################
        start = time()
        df_comments = classify_sentiment(df_comments)

        hours, mins, seconds = get_time(time() - start)
        logger.info(f"SENTIMENT CLASSIFICATION took: {hours} hours, {mins} mins, {seconds} seconds\n")

        #################### THOUGHTFULNESS CLASSIFICATION ####################
        start = time()
        df_comments_features = create_features(df_comments)
        df_comments_features_standardised = get_standardized_values(df_comments_features)
        comments_predictions = predict_thoughtfulness(df_comments_features_standardised)
        df_comments["isThoughtful"] = comments_predictions

        hours, mins, seconds = get_time(time() - start)
        logger.info(f"THOUGHTFUL CLASSIFICATION took: {hours} hours, {mins} mins, {seconds} seconds\n")

        #################### NOTEWORTHY CLASSIFICATION ####################
        start = time()
        df_comments["isNoteworthy"] = df_comments.apply(classify_noteworthy, axis=1)

        hours, mins, seconds = get_time(time() - start)
        logger.info(f"NOTEWORTHY CLASSIFICATION took: {hours} hours, {mins} mins, {seconds} seconds\n")

        #########################################################
        ############## END OF ML CLASSIFICATION #################
        #########################################################

        comments_data = df_comments.to_dict("index")
        reddit_comments.insert_many(comments_data[i] for i in range(len(comments_data)))

    logger.info(f"{year_folder} folder completed.")
