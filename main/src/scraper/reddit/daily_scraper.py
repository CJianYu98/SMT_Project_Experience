# Import packages
from dotenv import load_dotenv
from ....utils import file_utils
import datetime
import os

import praw
import math

# Load environment variables
load_dotenv()

# Access reddit API PRAW
try:
    reddit = praw.Reddit(
        client_id = os.getenv('CLIENT_ID'),
        client_secret = os.getenv('CLIENT_SECRET'),
        user_agent = os.getenv('USER_AGENT'),
        username = os.getenv('USERNAME'),
        password = os.getenv('PASSWORD')
    )
except:
    print('Failed to connect to Reddit API')


# Initialise scraping cut-off date
cutoff_days = int(os.getenv('CUTOFF_DAYS'))
start_datetime = datetime.datetime.now()
stop_datetime = start_datetime - datetime.timedelta(days = cutoff_days)

# Create storage dictionaries & initialise post counter
submissions_dict = {}
comments_dict = {}
counter = 0

# Iterate through list of newest submissions in selected Subreddit 
for sub in reddit.subreddit('Singapore').new(limit=math.inf):
    counter += 1

    # Stop loading new posts older than 2 weeks
    submission_created_datetime = datetime.datetime.fromtimestamp(sub.created_utc) #changes unixtimestamp to a readable format
    if stop_datetime > submission_created_datetime:
        break

    submission = vars(sub)
    submissions_dict[submission['id']] = submission
    print(f'Post {counter} saved.')

    # Load comments for each subreddit
    sub.comments.replace_more(limit = None)
    for comment in sub.comments.list():
        comment = vars(comment)
        comments_dict[comment['id']] = comment
    print(f'---> {len(sub.comments.list())} comments saved.')

    # Save data every 50 posts
    if counter % 50 == 0:
        file_utils.save_json(f'submissions/{start_datetime.date()}.json', submissions_dict)
        file_utils.save_json(f'comments/{start_datetime.date()}.json', comments_dict)

# Final save (Saves output in current directory containing python script, to edit later)
file_utils.save_json(f'./data/submissions/{start_datetime.date()}.json', submissions_dict)
file_utils.save_json(f'./data/comments/{start_datetime.date()}.json', comments_dict)