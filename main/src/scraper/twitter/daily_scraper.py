# Import packages
from dotenv import load_dotenv
import datetime
import os
import twint
import sys

# Load environment variables
load_dotenv()

# Initialise scraping cut-off date
cutoff_days = int(os.getenv('CUTOFF_DAYS'))
start_datetime = datetime.datetime.now()
stop_datetime = start_datetime - datetime.timedelta(days = cutoff_days)

# Configure up Twint
c = twint.Config()
c.Store_json = True # Store to json
c.Since = str(stop_datetime.strftime('%Y-%m-%d %H:%M:%S')) # Set end date for collection
c.Until = str(start_datetime.strftime('%Y-%m-%d %H:%M:%S')) # Set start date for collection
c.Retweets = True # Include retweets done by user
c.Near = 'Singapore' # Set geographic location to near Singapore
c.Lang = 'En' # Set language to english
c.Limit = sys.maxsize # Set tweet limit to unlimited
# c.Search = 'search term' # Set search term (optional)
c.Output = f'./main/src/scraper/twitter/data/{start_datetime.date()}.json' # Save output in current directory containing python script (edit later)

# Run Twint
twint.run.Search(c)

