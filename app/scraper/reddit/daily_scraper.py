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

# Create storage dictionaries & initialise post counter for tracking
submissions_dict = {}
counter = 0

# Iterate through list of newest submissions in selected Subreddit
for sub in reddit.subreddit("Singapore").new(limit=math.inf):
    counter += 1

    # Stop loading new posts older than 2 weeks
    submission_created_datetime = datetime.datetime.fromtimestamp(
        sub.created_utc
    )  # changes unixtimestamp to a readable format
    if stop_datetime > submission_created_datetime:
        # Stops scraping if  submission_created_datetime < stop_datetime
        # Note that earlier dates are considered smaller than later dates, i.e. 2022-01-14 < 2022-01-15
        break

    submission = vars(sub)  # Returns the __dict__ attribute of a given submission
    submission["comments"] = {}  # Initialise comments dictionary

    # Load comments for each submission
    sub.comments.replace_more(limit=None)
    for (
        comment
    ) in sub.comments.list():  # Loop through the list of comments for the submission
        comment = vars(comment)  # Returns the __dict__ attribute of a given submission
        submission["comments"][
            comment["id"]
        ] = comment  # Saves the comment to comments dictionary

    submissions_dict[submission["id"]] = submission
    print(f"Post {counter} saved [{len(sub.comments.list())} comments].")

# Save file
file_utils.save_json(
    f"./main/src/scraper/reddit/data/{start_datetime.date()}.json", submissions_dict
)
print("Daily scraping completed.")
