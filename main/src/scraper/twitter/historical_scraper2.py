# Import packages
from dotenv import load_dotenv
from ....utils import file_utils
import datetime
import os

import twint
# import time
# import json

# Load environment variables
load_dotenv()

# Initialise scraping cut-off date
cutoff_days = int(os.getenv('CUTOFF_DAYS'))
start_datetime = datetime.datetime.now()
stop_datetime = start_datetime - datetime.timedelta(days = cutoff_days)

# Set up Twint
c = twint.Config()    
c.Since = start_datetime # Set start date for collection
c.Until = stop_datetime # Set end date for collection
c.Store_csv = True # Store to json
c.Retweets = True # Include retweets done by user
c.Lang = 'en' # Set language
c.Limit = 100000 # Set tweet limit to 10k 
c.Near = 'Singapore' # Set geographic location to near Singapore

# Save output in current directory containing python script (edit later)
c.Output = f'./{start_datetime.date()}.csv' 
# c.Search = "search term" # Set search term

# Run Twint
twint.run.Search(c)

