# Import packages
import datetime
import os
import sys

import twint
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialise scraping cut-off date
cutoff_days = int(os.getenv("CUTOFF_DAYS"))
start_datetime = datetime.datetime.now()
stop_datetime = start_datetime - datetime.timedelta(days=cutoff_days)

# Configure up Twint
c = twint.Config()
c.Near = "Singapore"  # Set geographic location to near Singapore
c.Lang = "en"  # Set language to english
c.Limit = sys.maxsize  # Set tweet limit to unlimited
c.Retweets = True  # Include retweets done by user

c.Since = str(stop_datetime.strftime("%Y-%m-%d %H:%M:%S"))  # Set end date for collection
c.Until = str(start_datetime.strftime("%Y-%m-%d %H:%M:%S"))  # Set start date for collection

# Saves json to same folder as scraper (edit later)
c.Store_json = True  
c.Output = f"./app/scraper/twitter/{start_datetime.date()}.json"

# Run Twint
twint.run.Search(c)
