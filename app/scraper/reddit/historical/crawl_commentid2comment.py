import glob
import json
import math
import os
import time
from datetime import datetime

import pytz
import requests
import telegram_send
from dotenv import load_dotenv
from loguru import logger
from tqdm import tqdm

# Load environment variables
load_dotenv()

# Change to the actual file directory
os.chdir(os.path.dirname(os.path.realpath(__file__)))

# Add logger configurations
logger.add(
    "../../../logs/scraper/reddit/historical_scraper1.log",
    format="{time} {file} {level} {message}",
    level="DEBUG",
)

# Constants
TIMEZONE = pytz.timezone(os.getenv("TIMEZONE"))


def crawl_commentid2comment():
    telegram_send.send(
        messages=[
            f"REDDIT HISTORICAL (2020-2021) --> Comments crawling started at {datetime.now(TIMEZONE)}."
        ]
    )

    OUTPUT_DIR = "./comments"
    BATCH_SIZE = 200

    # Loop through all monthly comment id text files
    for afile in tqdm(sorted(glob.glob("data/*.txt"))):
        try:
            logger.debug(afile)
            filename = os.path.basename(afile)[:-4]
            OUTPUT_FILE = f"{OUTPUT_DIR}/{filename}_comments.txt"

            # Update saved cids
            crawled = set()
            if os.path.exists(OUTPUT_FILE):
                with open(OUTPUT_FILE) as fi:
                    for line in fi:
                        terms = [t.strip() for t in line.split("\t")]
                        crawled.add(",".join(eval(terms[1])))

            # Crawl comment data for given comment id
            with open(afile) as fi, open(f"{OUTPUT_FILE}", "a") as fo:
                for line in fi:
                    try:
                        sid, wrapped_comments = [t.strip() for t in line.split("\t")]
                        if comments := eval(wrapped_comments)["data"]:
                            for start_index in range(math.ceil(len(comments) / BATCH_SIZE)):
                                comments_to_crawl = comments[
                                    start_index
                                    * BATCH_SIZE : min(
                                        len(comments), (start_index + 1) * BATCH_SIZE
                                    )
                                ]
                                if not comments_to_crawl:
                                    continue
                                comm_params = ",".join(comments_to_crawl)
                                if comm_params in crawled:
                                    continue
                                params = {"ids": comm_params}

                                try:
                                    response = requests.get(
                                        "https://api.pushshift.io/reddit/comment/search",
                                        params=params,
                                    )
                                    if response.status_code == 200:
                                        jobj = json.loads(response.text)
                                        logger.debug(f"Comments for {params} crawled successfully.")
                                    time.sleep(5)
                                except Exception as e:
                                    logger.exception(e)
                                    continue
                                fo.write(f"{sid}\t{comments_to_crawl}\t{json.dumps(jobj)}\n")
                    except Exception as e:
                        telegram_send.send(
                            messages=[f"REDDIT HISTORICAL (2020-2021) --> Error: {e}"]
                        )
                        logger.exception(e)

            telegram_send.send(
                messages=[
                    f"REDDIT HISTORICAL (2020-2021) --> {afile}'s comments crawled successfully."
                ]
            )
            logger.debug(
                f"REDDIT HISTORICAL (2020-2021) --> {afile}'s comments crawled successfully."
            )
        except Exception as e:
            telegram_send.send(messages=[f"REDDIT HISTORICAL (2020-2021) --> Error: {e}"])
            logger.exception(e)

    telegram_send.send(
        messages=["REDDIT HISTORICAL (2020-2021) --> CommentID2Comments crawled completely."]
    )
