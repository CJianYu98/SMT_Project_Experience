# Import packages
import datetime
import json
import math
import os

import instaloader
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialise scraping cut-off date
# Integer 1514736000 represents epoch timestamp for 2018-01-01 00:00:00 (+8 GMT)
stop_datetime = datetime.datetime.fromtimestamp(1514736000) 

# Create an instance of Instaloader class
loader = instaloader.Instaloader(compress_json=False, download_comments=True, quiet=True)

# Enter your Instagram handle and password
ACCOUNT = os.getenv("INSTAGRAM_ACCOUNT")
PASSWORD = os.getenv("INSTAGRAM_PASSWORD")

# Upon successful authentication, you should see a message saying Authentication OK.
# Otherwise, check your login details
try:
    loader.login(ACCOUNT, PASSWORD)
    print("Authentication OK")
except:
    print("Error during authentication")

# Get profiles to scrape
profiles = json.load(open('./app/scraper/accounts_to_scrape/instagram.json'))

# Iterate through profiles
for p in profiles.values():
    # Get profile object
    profile = instaloader.Profile.from_username(loader.context, p)

    # Get all posts from the profile in a generator
    posts = profile.get_posts()

    for post in posts:
        # Download post if it is within historical period
        if post.date_local <= stop_datetime:
            break
        try:
            os.chdir('./app/scraper/instagram/data')
        except:
            pass
        loader.download_post(post, target=f"@{p}")
    print(f'Posts for @{p} scraped.')
print('Daily scraper completed.')
