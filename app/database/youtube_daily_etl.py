import json
import os
import time
import uuid
from datetime import datetime, timedelta
from pprint import pprint

import pandas as pd
import pytz
import telegram_send as tele
from dotenv import load_dotenv
from loguru import logger

from ..constants.social_media import YOUTUBE_COMMENT_FIELDS, YOUTUBE_VIDEO_FIELDS
from .connect import db
from .status_check import check_status

# Load environment variables
load_dotenv()

# Constants
YOUTUBE_DAILY_DATA_PATH = os.getenv("YOUTUBE_DAILY_DATA_PATH")
YOUTUBE_DAILY_ETL_LOG_FILE = os.getenv("YOUTUBE_DAILY_ETL_LOG_FILE")
DB_YOUTUBE_VIDEOS_COLLECTION = os.getenv("DB_YOUTUBE_VIDEOS_COLLECTION")
DB_YOUTUBE_COMMENTS_COLLECTION = os.getenv("DB_YOUTUBE_COMMENTS_COLLECTION")
SG_TIMEZONE = pytz.timezone("Asia/Singapore")
STATUS_CHECK_FILE = os.getenv("STATUS_CHECK_FILE")

# Add logger configurations
logger.add(
    YOUTUBE_DAILY_ETL_LOG_FILE,
    format="{time} {file} {level} {message}",
    level="DEBUG",
)

# Select MongoDB collection to work with
youtube_videos = db[DB_YOUTUBE_VIDEOS_COLLECTION]
youtube_comments = db[DB_YOUTUBE_COMMENTS_COLLECTION]

# Func for cleaning data columns
def date_str_to_dt(date: str) -> datetime:
    global crawled_date_str
    if "ago" in date:
        return datetime.strptime(crawled_date_str, "%Y-%m-%d")
    elif "Premiered" in date or "Premieres" in date:
        return datetime.strptime(date[10:], "%b %d, %Y")
    elif "Streamed" in date:
        return datetime.strptime(date[17:], "%b %d, %Y")
    else:
        return datetime.strptime(date, "%b %d, %Y")


def likes_str_to_int(likes: str) -> int:
    if likes == "LIKE":
        return 0
    elif "K" in likes or "k" in likes:
        return int(float(likes[:-1]) * 1000)
    else:
        return int(likes)


def views_str_to_int(views: str) -> int:
    if "waiting" in views:
        return 0
    else:
        return int(views[:-6].replace(",", ""))


# Check status for reddit daily collection
status_file = open(STATUS_CHECK_FILE)
status_jobj = json.load(status_file)
crawled_date_str = status_jobj["youtube"]["latest_collection_date"]
latest_collection_date = datetime.strptime(crawled_date_str, "%Y-%m-%d")
latest_etl_date = datetime.strptime(status_jobj["youtube"]["latest_etl_date"], "%Y-%m-%d")
curr_date = datetime.now(SG_TIMEZONE).date()

if (latest_collection_date.date() == curr_date) and (
    latest_etl_date.date() < latest_collection_date.date()
):
    start = time.time()
    logger.info(f"Starting daily ETL Youtube {latest_collection_date.date()}.json in GPU server")
    tele.send(
        messages=[f"Starting daily ETL Youtube {latest_collection_date.date()}.json in GPU server"]
    )

    # Retrieve all youtube video ids and delete all videos within date range
    end_date = latest_collection_date
    start_date = end_date - timedelta(days=13)
    db_query = {"date_uploaded": {"$gte": start_date, "$lte": end_date}}
    videos = list(youtube_videos.find(db_query))
    vid_ids = [vid["id"] for vid in videos]
    youtube_videos.delete_many(db_query)

    # Delete all comments under a video
    for v_id in vid_ids:
        youtube_comments.delete_many({"vid_id": v_id})

    # Store all the comments
    comments = []

    with open(f"{YOUTUBE_DAILY_DATA_PATH}/{latest_collection_date.date()}.json") as f:
        jobj = json.load(f)

    for channel, data in jobj.items():
        if data:
            # Rename column names
            df = pd.DataFrame(data)
            col_names = {col: col.lower() for col in df.columns}
            col_names["Date Uploaded"] = "date_uploaded"
            df.rename(columns=col_names, inplace=True)

            # Process/transform data fields
            df["date_uploaded"] = df["date_uploaded"].apply(date_str_to_dt)
            df["id"] = df.apply(lambda x: uuid.uuid4().hex, axis=1)
            df["channel"] = channel
            df["views"] = df["views"].apply(views_str_to_int)
            df["likes"] = df["likes"].apply(likes_str_to_int)

            yt_videos = df.drop("comments", axis=1)

            # Inserting youtube videos data
            yt_vid_data = yt_videos.to_dict(orient="index")
            youtube_videos.insert_many([yt_vid_data[i] for i in range(len(yt_vid_data))])

            # Retrieving youtube comments data for each video
            for i in range(len(df)):
                if df.iloc[i]["comments"] != None and df.iloc[i]["comments"] != []:
                    for cmt in df.iloc[i]["comments"]:
                        comments.append(
                            {"id": uuid.uuid4().hex, "vid_id": df.iloc[i]["id"], "text": cmt}
                        )
    # Inserting youtube videos data
    youtube_comments.insert_many(comments)

    # Update status file
    status_jobj["youtube"]["latest_etl_date"] = datetime.now().date().strftime("%Y-%m-%d")
    with open(STATUS_CHECK_FILE, "w") as f:
        json.dump(status_jobj, f, indent=4)

    duration = time.time() - start
    logger.info(
        f"Daily ETL for Youtube {latest_collection_date.date()}.json has completed, time taken: {duration}"
    )
    tele.send(
        messages=[
            f"Daily ETL for Youtube {latest_collection_date.date()}.json has completed, time taken: {duration}"
        ]
    )
