import json
import os
import time
from datetime import datetime, timezone

import requests
from dotenv import load_dotenv
from loguru import logger

# Load environment variables
load_dotenv()


def monthly_crawl_submissions():
    OUTPUT_DIR = "./app/scraper/reddit/historical_2/yyyymm"
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Start scraping from given date
    last_created_utc = os.getenv("SCRAPE_FROM_DATE")
    while True:
        logger.debug(f"last_created_utc: {last_created_utc}")
        params = {
            "subreddit": "singapore",
            "sort": "asc",
            "metadata": "true",
            "after": last_created_utc,
            "size": 100,  # Max 500
        }

        try:
            response = requests.get(
                "https://api.pushshift.io/reddit/search/submission/", params=params
            )
        except:
            logger.exception("Http Requests Error.")
            time.sleep(15)
            continue

        jobj = json.loads(response.text)
        for submission in jobj["data"]:
            created_utc = submission["created_utc"]
            yyyymm = datetime.fromtimestamp(created_utc, timezone.utc).strftime("%Y%m")
            with open(f"{OUTPUT_DIR}/{yyyymm}.jsonl", "a") as fo:
                fo.write(json.dumps(submission) + "\n")

        try:
            submission_cnt = len(jobj["data"])
        except:
            logger.exception("No data in Submission object.")
            break
        logger.debug(f"data size: {submission_cnt}")

        try:
            last_created_utc = jobj["data"][-1]["created_utc"]
            time.sleep(2)
        except:
            print(">>> Submission Crawling Complete.")
            break
