# Import packages
import datetime
import json
import math
import os

import boto3
import praw
import telegram_send
from dotenv import load_dotenv


# Utility functions for scraper
def save_json(filename: str, new_dict: dict):
    """
    Convert data into a json format and save into local folder.

    Args:
        filename (str): File name
        new_dict (dict): Dictionary containing the scraped data
    """
    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(new_dict, f, ensure_ascii=False, indent=4, default=str)
    except Exception as e:

        telegram_send.send(messages=[f"Error saving {filename} to local folder."])


def upload_files(file_name: str, bucket: str, object_name=None, args=None):
    """
    Upload json data file into AWS S3 bucket. Sends telegram notification afterwards.

    Args:
        file_name (str): File name
        bucket (str): AWS S3 bucket name
        object_name (str, optional): AWS S3 object name. Defaults to None.
        args (str, optional): Extra arguments. Defaults to None.
    """
    if object_name is None:
        object_name = file_name
    try:
        s3_client.upload_file(file_name, bucket, object_name, ExtraArgs=args)
        telegram_send.send(messages=[f"{file_name} has been uploaded to {S3_BUCKET_NAME}."])
    except Exception as e:
        telegram_send.send(messages=[f"{file_name} failed to upload to {S3_BUCKET_NAME}.", f"{e}"])


telegram_send.send(messages=[f"Reddit daily scraping started at {datetime.datetime.now()}."])

# Load environment variables and create constant variables
load_dotenv("/home/ubuntu/SMT_Project_Experience/.env")
S3_BUCKET_NAME = "smt483tls-reddit-daily-bucket"

# Intialize S3 client
s3_client = boto3.client("s3")

# Access reddit API PRAW
try:
    reddit = praw.Reddit(
        client_id=os.getenv("REDDIT_CLIENT_ID"),
        client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
        user_agent=os.getenv("REDDIT_USER_AGENT"),
        username=os.getenv("REDDIT_USERNAME"),
        password=os.getenv("REDDIT_PASSWORD"),
    )
except:
    telegram_send.send(messages=["Failed to connect to Reddit API"])

# Initialise scraping cut-off date
cutoff_days = int(os.getenv("CUTOFF_DAYS"))
start_datetime = datetime.datetime.now()
stop_datetime = start_datetime - datetime.timedelta(days=cutoff_days)

# Create storage dictionaries & initialise post counter for tracking
submissions_dict = {}
counter = 0

# Create filename for the saved data
filename = f"/home/ubuntu/SMT_Project_Experience/app/scraper/reddit/daily_data/{start_datetime.date()}.json"

# Iterate through list of newest submissions in selected Subreddit
for sub in reddit.subreddit("Singapore").new(limit=math.inf):

    # Stop loading new posts older than 2 weeks
    # Note that earlier dates are considered smaller than later dates
    # i.e. 2022-01-14 < 2022-01-15
    submission_created_datetime = datetime.datetime.fromtimestamp(sub.created_utc)
    if stop_datetime > submission_created_datetime:
        break

    counter += 1

    # Save the serialized version of a given submission in dict format
    submission = vars(sub)

    # Getting comments
    submission["comments"] = {}  # Initialise comments dictionary within submission
    sub.comments.replace_more(limit=None)  # Load comments for each submission

    # Loop through the list of comments for the submission
    for comment in sub.comments.list():
        comment = vars(comment)
        submission["comments"][comment["id"]] = comment

    # Store current submission record
    submissions_dict[submission["id"]] = submission

# Save file
save_json(filename, submissions_dict)

# Upload to S3 and delete file from local folder afterwards
upload_files(filename, S3_BUCKET_NAME, f"{start_datetime.date()}.json")
if os.path.exists(filename):
    os.remove(filename)
    telegram_send.send(messages=[f"{filename} removed from local folder successfully."])
else:
    telegram_send.send(messages=[f"Failed to remove {filename} from local folder."])

telegram_send.send(
    messages=[
        f"Reddit daily scraping for {start_datetime.strftime('%Y-%m-%d')} completed. {counter} posts scraped."
    ]
)
