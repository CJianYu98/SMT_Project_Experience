# Installation: Install dev version of snscrape to get more attributes from Twitter scraping
# !pip install git+https://github.com/JustAnotherArchivist/snscrape.git

import math
import os
from datetime import datetime, timedelta

import pandas as pd
import pytz
import snscrape.modules.twitter as sntwitter
import telegram_send
from dotenv import load_dotenv
from loguru import logger

# Load environment variables
load_dotenv()

# Constants and variables
S3_BUCKET_NAME = os.getenv("S3_TWITTER_HISTORICAL_BUCKET_NAME")
TIMEZONE = pytz.timezone(os.getenv("TIMEZONE"))
sg_datetime = datetime.now(TIMEZONE)

# Set parameters used to retrieve tweets
from_date = "2018-01-01"  # Inclusive of first date
end_date = "2019-01-01"  # Exclusive of this date
max_tweet = math.inf  # For yearly scraping, set to >1mil
location = "Singapore"
year = from_date.split("-")[0]

tele_start_msg = f"TWITTER HISTORICAL --> Historical data crawling started from {from_date} to {end_date} at {sg_datetime}"
tele_end_msg = "TWITTER HISTORICAL --> \n"

os.makedirs("./historical_data", exist_ok=True)

try:
    telegram_send.send(messages=[tele_start_msg])
    logger.info(f"Historical data crawling started from {from_date} to {end_date} at {sg_datetime}")

    # Using TwitterSearchScraper to scrape data and append tweets to list
    tweets_list = []

    for i, tweet in enumerate(
        sntwitter.TwitterSearchScraper(
            "near:"
            + location
            + " lang:en since:"
            + from_date
            + " until:"
            + end_date
            + "-filter:retweets"
        ).get_items()
    ):

        tweets_list.append(
            [
                tweet.date,
                tweet.id,
                tweet.username,
                tweet.content,
                tweet.url,
                tweet.user.verified,
                tweet.profileImageUrl,
                tweet.replyCount,
                tweet.retweetCount,
                tweet.likeCount,
                tweet.quoteCount,
                tweet.media,
            ]
        )

        if i > max_tweet:
            tele_end_msg += f"maximum hit, scrape again from date: {tweet.date}"
            break

        # Creating a dataframe from the tweets list above
        tweets_df = pd.DataFrame(
            tweets_list,
            columns=[
                "Datetime",
                "Tweet Id",
                "Username",
                "Text",
                "URL",
                "isVerified",
                "Profile URL",
                "Reply Count",
                "Retweet Count",
                "Like Count",
                "Quote Count",
                "Media",
            ],
        )
        output_file = tweets_df.to_csv(f"./historical_data/{year}.csv")

    tele_end_msg += (
        f"Historical data crawling started from {from_date} to {end_date} is fully completed"
    )
    logger.info(
        f"Historical data crawling started from {from_date} to {end_date} is fully completed"
    )

except Exception as e:
    tele_end_msg += f"Error occured.\n{e}\n"
    logger.exception("Error occured.")
finally:
    telegram_send.send(messages=[tele_end_msg])
