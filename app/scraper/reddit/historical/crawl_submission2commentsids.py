import glob
import json
import os
import time
from datetime import datetime

import pytz
import requests
import telegram_send
from loguru import logger
from dotenv import load_dotenv
from tqdm import tqdm

# Load environment variables
load_dotenv()

# Change to the actual file directory
os.chdir(os.path.dirname(os.path.realpath(__file__)))

# Add logger configurations
logger.add(
    "../../../logs/scraper/reddit/daily_scraper.log",
    format="{time} {file} {level} {message}",
    level="DEBUG",
)

# Constants
TIMEZONE = pytz.timezone(os.getenv("TIMEZONE"))


def crawl_submission2commentsids():
    telegram_send.send(
        messages=[
            f"REDDIT HISTORICAL --> Comment IDs crawling for 2020-2021 started at {datetime.now(TIMEZONE)}."
        ]
    )

    OUTPUT_DIR = "./data"

    # Loop through monthly submission jsonl files
    for afile in tqdm(sorted(glob.glob(f"{OUTPUT_DIR}/*.jsonl"))):
        filename = os.path.basename(afile)[:-6]
        OUTPUT_FILE = f"{OUTPUT_DIR}/{filename}_sid_cids.txt"

        # Update saved sids (this chunk can be deleted)
        crawled_sids = set()
        if os.path.exists(OUTPUT_FILE):
            with open(OUTPUT_FILE) as fi:
                for line in fi:
                    terms = [t.strip() for t in line.split("\t")]
                    crawled_sids.add(terms[0])

        # Crawl comment ids for given submission id
        with open(afile) as fi, open(f"{OUTPUT_DIR}/{filename}_sid_cids.txt", "a") as fo:
            for line in fi:
                jobj = json.loads(line)
                sid = jobj["id"]
                if sid in crawled_sids:
                    continue
                try:
                    response = requests.get(
                        f"https://api.pushshift.io/reddit/submission/comment_ids/{sid}"
                    )
                    if response.status_code == 200:
                        jobj = json.loads(response.text)
                        logger.debug(f"Comment IDs for submission {sid} crawled successfully.")
                    time.sleep(3)
                except Exception as e:
                    logger.exception(e)
                    continue
                fo.write(f"{sid}\t{json.dumps(jobj)}\n")

        telegram_send.send(messages=[f"REDDIT HISTORICAL --> {afile}'s cids crawled successfully."])
        logger.debug(f"REDDIT HISTORICAL --> {afile}'s cids crawled successfully.")

    telegram_send.send(messages=["REDDIT HISTORICAL --> Submission2CommentIDs for 2020-2021 crawled completely."])
