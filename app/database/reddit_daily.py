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
    REDDIT_DAILY_COMMENT_FIELDS,
    REDDIT_DAILY_SUBMISSION_FIELDS,
)
from .connect import db

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
    start = time.time()
    logger.info(f"Starting to ETL Reddit {file}")
    tele.send(messages=[f"Starting to ETL Reddit {file}"])

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
    df_sub.head()
    sub_data = df_sub.to_dict("index")
    reddit_submissions.insert_many(sub_data[i] for i in range(len(sub_data)))

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
    reddit_comments.insert_many(comments)

    logger.info(f"Num submissions: {len(sub_data)}, Num comments: {len(comments)}")

    duration = time.time() - start
    logger.info(f"ETL Reddit {file} took {duration}")
    tele.send(messages=[f"ETL Reddit {file} took {duration}"])
    
