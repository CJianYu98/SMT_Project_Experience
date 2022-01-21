# Import packages
import datetime
import sys

import twint
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialise scraping start date
start_datetime = datetime.datetime.now()

# Set up Twint
c = twint.Config()
c.Near = "Singapore"  # Set geographic location to near Singapore
c.Lang = "en"  # Set language to english
c.Limit = sys.maxsize  # Set tweet limit to unlimited
c.Retweets = True  # Include retweets done by user

c.Since = "2018-01-01 00:00:00"  # Set end date for collection
c.Until = str(start_datetime.strftime("%Y-%m-%d %H:%M:%S"))  # Set start date for collection

# Saves json to same folder as scraper (edit later)
c.Store_json = True 
c.Output = "./app/scraper/twitter/historical.json"

# Run Twint
twint.run.Search(c)
