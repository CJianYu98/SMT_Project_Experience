import os
from datetime import datetime, timedelta

from fastapi import APIRouter, HTTPException

from ..dao.dao import get_social_media_feed_stats
from ..schema.user_filter import Filter

router = APIRouter(prefix="/social-media-feed", tags=["social_media_feed"])

# Declare MongoDB collection names to interact with
FB_POSTS = os.getenv("DB_FACEBOOK_POSTS_COLLECTION")
FB_COMMENTS = os.getenv("DB_FACEBOOK_COMMENTS_COLLECTION")
TWITTER_TWEETS = os.getenv("DB_TWIITER_TWEETS_COLLECTION")
TWITTER_COMMENTS = os.getenv("DB_TWITTER_COMMENTS_COLLECTION")
REDDIT_SUBMISSIONS = os.getenv("DB_REDDIT_SUBMISSIONS_COLLECTION")
REDDIT_COMMENTS = os.getenv("DB_REDDIT_COMMENTS_COLLECTION")
YOUTUBE_VIDEOS = os.getenv("DB_YOUTUBE_VIDEOS_COLLECTION")
YOUTUBE_COMMENTS = os.getenv("DB_YOUTUBE_COMMENTS_COLLECTION")


def calc_aggregated_stats(posts_data, comments_data):
    """
    Util func to calculate aggregated stats for social media feed

    Args:
        posts_data (dict): Posts data (post refers to posts, tweets, submissions, videos)
        comments_data (dict): Comments data

    Returns:
        dict: Dict with mentions count, sentiment counts list and emotion counts list
    """

    res = {
        "mentions": posts_data.get("mentions", 0) + comments_data.get("mentions", 0),
        "sentiment": [],
        "emotions": []
    }

    sentiments = ["positive", "neutral", "negative"]
    emotions = ["anger", "fear", "joy", "sadness", "neutral"]

    for sentiment in sentiments:
        res["sentiment"].append({
            "sentiment": sentiment,
            "count": posts_data.get(f'{sentiment}_sentiment', 0) + comments_data.get(f'{sentiment}_sentiment', 0)
        })
    
    for emotion in emotions:
        res["emotions"].append({
            "emotion": emotion,
            "count": posts_data.get(f'{emotion}_emotion', 0) + comments_data.get(f'{emotion}_emotion', 0)
        })

    return res


@router.post("/get-all-aggregated-stats")
def get_all_aggregated_stats(filter: Filter):
    """
    To get aggregated social media feed mentions, sentiments and emotions stats for all platforms

    Args:
        filter (Filter): JSON request body (user's filter options)

    Returns:
        Pydantic Model: JSON response object
    """

    res = {}

    if "facebook" in filter.platforms:
        fb_posts_data = get_social_media_feed_stats(filter, FB_POSTS)
        fb_comments_data = get_social_media_feed_stats(filter, FB_COMMENTS)
        res['facebook'] = calc_aggregated_stats(fb_posts_data, fb_comments_data)
    if "twitter" in filter.platforms:
        twit_tweets_data = get_social_media_feed_stats(filter, TWITTER_TWEETS)
        twit_comments_data = get_social_media_feed_stats(filter, TWITTER_COMMENTS)
        res['twitter'] = calc_aggregated_stats(twit_tweets_data, twit_comments_data)
    if "reddit" in filter.platforms:
        reddit_submissions_data = get_social_media_feed_stats(filter, REDDIT_SUBMISSIONS)
        reddit_comments_data = get_social_media_feed_stats(filter, REDDIT_COMMENTS)
        res['reddit'] = calc_aggregated_stats(reddit_submissions_data, reddit_comments_data)
    if "youtube" in filter.platforms:
        youtube_videos_data = get_social_media_feed_stats(filter, YOUTUBE_VIDEOS)
        youtube_comments_data = get_social_media_feed_stats(filter, YOUTUBE_COMMENTS)
        res['youtube'] = calc_aggregated_stats(youtube_videos_data, youtube_comments_data)
    
    return res


