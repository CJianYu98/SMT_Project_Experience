# Import packages
from dotenv import load_dotenv
from ....utils import file_utils
import datetime
import os
import json
import praw
import math
import pprint

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

# Create new json file with current date as filename
new_filename = str(start_datetime.date())
new_filepath = f'./main/src/scraper/reddit/data/{new_filename}.json'
file_utils.create_json(new_filepath)

# Initialise post counter for tracking
counter = 0

# Read newly created json file
with open(new_filepath, 'a') as file:

    # Iterate through list of newest submissions in selected Subreddit 
    for sub in reddit.subreddit('Singapore').new(limit=math.inf):
        counter += 1

        # Stop loading new posts older than 2 weeks
        submission_created_datetime = datetime.datetime.fromtimestamp(sub.created_utc) # changes unixtimestamp to a readable format
        if  submission_created_datetime < stop_datetime: 
            # Stops scraping if  submission_created_datetime < stop_datetime
            # Note that earlier dates are considered smaller than later dates, i.e. 2022-01-14 < 2022-01-15
            break

        submission = vars(sub) # Returns the __dict__ attribute of a given submission
        submission['comments'] = {} # Initialise comments dictionary
        
        # Load comments for each submission
        sub.comments.replace_more(limit = None)
        for comment in sub.comments.list(): # Loop through the list of comments for the submission
            comment = vars(comment) # Returns the __dict__ attribute of a given submission
            submission['comments'][comment['id']] = comment # Saves the comment to comments dictionary

        print(f'Post {counter} saved [{len(sub.comments.list())} comments].')

        # Append individual submission to json file
        json.dump(submission, file, ensure_ascii=False, indent=4, default=str)