import json
import os
from dotenv import load_dotenv
from loguru import logger

from .connect import client
from ..constants.social_media import REDDIT_COMMENTS_FIELDS, REDDIT_SUBMISSION_FIELDS


# Load environment variables
load_dotenv()

# Constants
REDDIT_HISTORICAL_DATA_PATH = os.getenv("REDDIT_HISTORICAL_DATA_PATH")

# Select MongoDB collection to work with
reddit_submissions = client.smt483.reddit_submissions
reddit_comments = client.smt483.reddit_comments

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
            record = lines[i].split('\t')[2]
            comments = json.loads(record)['data']

            for j in range(len(comments)):
                temp = {}
                for field in REDDIT_COMMENTS_FIELDS:
                    try:
                        temp[field] = jobj['data'][j][field]
                    except:
                        continue
                comments_data.append(temp)

        reddit_comments.insert_many(comments_data)
    logger.info(f"{year_folder} folder completed.")