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
c.Store_json = True  # Store to json
c.Since = "2018-01-01 00:00:00"  # Set end date for collection
c.Until = str(start_datetime.strftime("%Y-%m-%d %H:%M:%S"))  # Set start date for collection
c.Retweets = True  # Include retweets done by user
c.Near = "Singapore"  # Set geographic location to near Singapore
c.Lang = "en"  # Set language to english
c.Limit = sys.maxsize  # Set tweet limit to unlimited
# c.Search = 'search term' # Set search term (optional)
c.Output = "./main/src/scraper/twitter/data/historical.json"  # Save output in current directory containing python script (edit later)

# Run Twint
twint.run.Search(c)
