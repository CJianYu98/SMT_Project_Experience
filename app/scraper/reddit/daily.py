# Import packages
import datetime
import json
import math
import os

import praw
import telegram_send
from dotenv import load_dotenv

# Load environment variables
load_dotenv("/home/ubuntu/SMT_Project_Experience/.env")


def save_json(filename, new_dict):
    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(new_dict, f, ensure_ascii=False, indent=4, default=str)
    except Exception as e:
        telegram_send.send(messages=[f"Error saving {filename}."])


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
    print("Failed to connect to Reddit API")

# Initialise scraping cut-off date
cutoff_days = int(os.getenv("CUTOFF_DAYS"))
start_datetime = datetime.datetime.now()
stop_datetime = start_datetime - datetime.timedelta(days=cutoff_days)

# Create storage dictionaries & initialise post counter for tracking
submissions_dict = {}
counter = 0

telegram_send.send(messages=[f"Reddit daily scraping started at {start_datetime}."])

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
save_json(
    f"/home/ubuntu/SMT_Project_Experience/app/scraper/reddit/daily_data/{start_datetime.date()}.json",
    submissions_dict,
)
telegram_send.send(
    messages=[
        f"Reddit daily scraping for {start_datetime.strftime('%Y-%m-%d')} completed. {counter} posts scraped."
    ]
)
