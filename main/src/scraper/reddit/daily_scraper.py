import praw
import pandas as pd
import datetime
import math
from dotenv import load_dotenv
import os
from ....utils import file_utils

# Load environment variables
load_dotenv()

# Access reddit API PRAW
try:
    reddit = praw.Reddit(
        client_id = os.getenv('client_id'),
        client_secret = os.getenv('client_secret'),
        user_agent = os.getenv('user_agent'),
        username = os.getenv('username'),
        password = os.getenv('password')
    )
except:
    print('Failed to connect to Reddit API')


# Initialise scraping cut-off date
scraping_cut_off_period = int(os.getenv('scraping_cut_off_period'))
cut_off_datetime = datetime.datetime.now() - datetime.timedelta(days = scraping_cut_off_period)

# Create storage dictionaries & initialise post counter
submissions_dict = {}
comments_dict = {}
counter = 0

# Iterate through list of newest submissions in selected Subreddit 
for sub in reddit.subreddit("Singapore").new(limit=math.inf):
    counter += 1
    counter2 = 0
    
    # Stop loading new posts older than 2 weeks
    submission_created_datetime = datetime.datetime.fromtimestamp(sub.created_utc) #changes unixtimestamp to a readable format
    if cut_off_datetime > submission_created_datetime:
        break

    submission = vars(sub)
    submissions_dict[submission['id']] = submission
    print(f'Post {counter} saved.')

    # Load comments for each subreddit
    sub.comments.replace_more(limit = None)
    for comment in sub.comments.list():
        counter2 += 1
        comment = vars(comment)
        comments_dict[comment['id']] = comment
    print(f'---> {len(sub.comments.list())} comments saved.')

    # Save data every 50 posts
    if counter % 50 == 0:
        file_utils.save_json('submissions.json', submissions_dict)
        file_utils.save_json('comments.json', comments_dict)

# Final save (for now this saves to the SMT_Project_Experience folder if run)
file_utils.save_json('submissions.json', submissions_dict)
file_utils.save_json('comments.json', comments_dict)