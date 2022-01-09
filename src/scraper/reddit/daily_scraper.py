import praw
import pandas as pd
import json 
import datetime
import math

# Access reddit API PRAW
try:
    reddit = praw.Reddit(client_id='PUMTWg7cm-mhKQ',
                        client_secret='f_SDu_F3C5Z4epNT-RKMMfY9KqlEOQ',
                        user_agent='smt203',
                        username='smt203css',
                        password='ilovesmt203!haha')
except:
    print('Failed to connect to Reddit API')

# Create storage dictionaries
submissions_dict = {}
comments_dict = {}
cut_off_datetime = datetime.datetime.now() - datetime.timedelta(days = 14)
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

    sub.comments.replace_more(limit = None)

    for comment in sub.comments.list():
        counter2 += 1
        comment = vars(comment)
        comments_dict[comment['id']] = comment
    print(f'---> {len(sub.comments.list())} comments saved.')

    # Save data every 50 posts
    if counter % 50 == 0:
        try:
            with open('submissions.json', 'w', encoding='utf-8') as f:
                json.dump(submissions_dict, f, ensure_ascii=False, indent=4, default=str)
        except:
            print('Error saving submissions.json.')

        try:
            with open('comments.json', 'w', encoding='utf-8') as f:
                json.dump(comments_dict, f, ensure_ascii=False, indent=4, default=str)
        except:
            print('Error saving comments.json.')

# Final save
try:
    with open('submissions.json', 'w', encoding='utf-8') as f:
        json.dump(submissions_dict, f, ensure_ascii=False, indent=4, default=str)
except:
    print('Error saving submissions.json.')

try:
    with open('comments.json', 'w', encoding='utf-8') as f:
        json.dump(comments_dict, f, ensure_ascii=False, indent=4, default=str)
except:
    print('Error saving comments.json.')