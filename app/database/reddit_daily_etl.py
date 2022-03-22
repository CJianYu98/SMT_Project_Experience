import json
import os
import time
from datetime import datetime, timedelta
from pprint import pprint

import pytz
import telegram_send as tele
from dotenv import load_dotenv
from loguru import logger

from ..constants.social_media import (
    REDDIT_DAILY_COMMENT_FIELDS,
    REDDIT_SUBMISSION_FIELDS,
)
from .connect import db
from .status_check import check_status

# Load environment variables
load_dotenv()

# Constants
REDDIT_DAILY_DATA_PATH = os.getenv("REDDIT_DAILY_DATA_PATH")
REDDIT_DAILY_ETL_LOG_FILE = os.getenv("REDDIT_DAILY_ETL_LOG_FILE")
DB_REDDIT_SUBMISSIONS_COLLECTION = os.getenv("DB_REDDIT_SUBMISSIONS_COLLECTION")
DB_REDDIT_COMMENTS_COLLECTION = os.getenv("DB_REDDIT_COMMENTS_COLLECTION")
STATUS_CHECK_FILE = os.getenv("STATUS_CHECK_FILE")
SG_TIMEZONE = pytz.timezone('Asia/Singapore')

# Add logger configurations
logger.add(
    REDDIT_DAILY_ETL_LOG_FILE,
    format="{time} {file} {level} {message}",
    level="DEBUG",
)

# Select MongoDB collection to work with
reddit_submissions = db[DB_REDDIT_SUBMISSIONS_COLLECTION]
reddit_comments = db[DB_REDDIT_COMMENTS_COLLECTION]

# Check status for reddit daily collection
status_file = open(STATUS_CHECK_FILE)
status_jobj = json.load(status_file)
latest_collection_date = datetime.strptime(
    status_jobj["reddit"]["latest_collection_date"], "%Y-%m-%d"
)
curr_date = datetime.now(SG_TIMEZONE).date()

if latest_collection_date.date() == curr_date:
    start = time.time()
    logger.info(f"Starting daily ETL Reddit {file}")
    tele.send(messages=[f"Starting daily ETL Reddit {file} in GPU server"])

    f = open(f"{REDDIT_DAILY_DATA_PATH}/{latest_collection_date}.json")
    jobj = json.load(f)

    # To store new data
    submission_data = []
    comments_data = []

    # Delete all submissions within date range
    date = file[:-5]
    end_date = datetime.strptime(date, "%Y-%m-%d")
    start_date = end_date - timedelta(days=14)
    db_query = {"created_datetime": {"$gte": start_date, "$lte": end_date}}
    reddit_submissions.delete_many(db_query)

    for sub_id, data in jobj.items():
        logger.info(f"Reading data for Submission {sub_id}")

        # Create a submission data record
        sub = {}
        for field in REDDIT_SUBMISSION_FIELDS:
            try:
                if field == "created_utc":
                    dt = datetime.fromtimestamp(data[field]).astimezone(pytz.UTC)
                    sub["created_datetime"] = dt
                else:
                    sub[field] = data[field]
            except:
                continue
        submission_data.append(sub)

        # Delete all comments under a submission, then bulk insert all comments instead (faster time performance)
        reddit_comments.delete_many({"submission_id": sub_id})

        # Create comment data record
        comments = data["comments"]
        for cid, c_data in comments.items():
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
            comments_data.append(comment)

    if submission_data:
        reddit_submissions.insert_many(submission_data)
    if comments_data:
        reddit_comments.insert_many(comments_data)

    duration = time.time() - start
    tele.send(messages=[f"Daily ETL Reddit {file} took {duration}"])
