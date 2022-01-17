# Import packages
import datetime
import math
import os

import praw
from dotenv import load_dotenv

from ...utils import file_utils

# Load environment variables
load_dotenv()

# Access reddit API PRAW
try:
    reddit = praw.Reddit(
        client_id=os.getenv("CLIENT_ID"),
        client_secret=os.getenv("CLIENT_SECRET"),
        user_agent=os.getenv("USER_AGENT"),
        username=os.getenv("USERNAME"),
        password=os.getenv("PASSWORD"),
    )
except:
    print("Failed to connect to Reddit API")

# Initialise scraping cut-off date
cutoff_days = int(os.getenv("CUTOFF_DAYS"))
start_datetime = datetime.datetime.now()
stop_datetime = start_datetime - datetime.timedelta(days=cutoff_days)

# Create storage dictionaries
submissions_dict = {}

# Iterate through list of newest submissions in selected Subreddit
for sub in reddit.subreddit("Singapore").new(limit=math.inf):

    # Stop loading new posts older than 2 weeks
    # Note that earlier dates are considered smaller than later dates, i.e. 2022-01-14 < 2022-01-15
    submission_created_datetime = datetime.datetime.fromtimestamp(sub.created_utc)
    if stop_datetime > submission_created_datetime:
        break

    # Initialise comments dictionary
    submission = vars(sub)
    submission["comments"] = {}

    # Load comments for each submission
    sub.comments.replace_more(limit=None)

    # Loop through the list of comments for the submission
    for comment in sub.comments.list():
        comment = vars(comment)
        submission["comments"][comment["id"]] = comment

    # Store current submission record
    submissions_dict[submission["id"]] = submission

# Save file
file_utils.save_json(f"./app/scraper/reddit/data/{start_datetime.date()}.json", submissions_dict)
print("Daily scraping completed.")
