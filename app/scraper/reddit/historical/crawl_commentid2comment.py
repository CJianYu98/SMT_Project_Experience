import glob
import json
import math
import os
import time

import requests
from loguru import logger
from tqdm import tqdm


def crawl_commentid2comment():
    OUTPUT_DIR = "./app/scraper/reddit/historical_2/yyyymm"
    BATCH_SIZE = 200

    # Loop through all monthly comment id text files
    for afile in tqdm(sorted(glob.glob("yyyymm/*.txt"))):
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
            for l_index, line in enumerate(fi):
                logger.debug(l_index)
                print(">>>", line)
                sid, wrapped_comments = [t.strip() for t in line.split("\t")]
                comments = eval(wrapped_comments)["data"]
                print(">>>", comments)
                time.sleep(15)
                if comments:
                    #                 logger.debug('?')
                    for start_index in range(math.ceil(len(comments) / BATCH_SIZE)):
                        comments_to_crawl = comments[
                            start_index
                            * BATCH_SIZE : min(len(comments), (start_index + 1) * BATCH_SIZE)
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
                            jobj = json.loads(response.text)
                        except:
                            logger.exception("conn error?")
                            time.sleep(15)
                            continue
                        fo.write(f"{sid}\t{comments_to_crawl}\t{json.dumps(jobj)}\n")
                        time.sleep(1)
