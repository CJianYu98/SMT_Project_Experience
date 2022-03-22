import json
import os
from datetime import datetime, timedelta
from pprint import pprint

import pytz
from dotenv import load_dotenv
from loguru import logger

from ..constants.social_media import REDDIT_COMMENT_FIELDS, REDDIT_SUBMISSION_FIELDS
from .connect import db

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

        reddit_submissions.insert_many(submission_data)

    # # Inserting reddit comments data
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

        reddit_comments.insert_many(comments_data)
    logger.info(f"{year_folder} folder completed.")
