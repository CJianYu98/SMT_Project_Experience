import glob
import json
import os
import time

import requests
from loguru import logger
from tqdm import tqdm


def crawl_submission2commentsids():
    OUTPUT_DIR = "./app/scraper/reddit/historical_2/yyyymm"

    # Loop through monthly submission jsonl files
    for afile in tqdm(sorted(glob.glob("yyyymm/*.jsonl"))):
        logger.debug(afile)
        filename = os.path.basename(afile)[:-6]
        OUTPUT_FILE = f"{OUTPUT_DIR}/{filename}_sid_cids.txt"

        # Update saved sids
        crawled_sids = set()
        if os.path.exists(OUTPUT_FILE):
            with open(OUTPUT_FILE) as fi:
                for line in fi:
                    terms = [t.strip() for t in line.split("\t")]
                    crawled_sids.add(terms[0])

        # Crawl comment ids for given submission id
        with open(afile) as fi, open(f"{OUTPUT_DIR}/{filename}_sid_cids.txt", "a") as fo:
            for l_index, line in enumerate(fi):
                logger.debug(l_index)
                jobj = json.loads(line)
                sid = jobj["id"]
                if sid in crawled_sids:
                    continue
                try:
                    response = requests.get(
                        f"https://api.pushshift.io/reddit/submission/comment_ids/{sid}"
                    )
                    jobj = json.loads(response.text)
                    print(">>>", jobj)
                except:
                    logger.exception("Connection Error?")
                    time.sleep(15)
                    continue
                fo.write(f"{sid}\t{json.dumps(jobj)}\n")
                time.sleep(1)
