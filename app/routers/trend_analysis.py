import copy
import os
from datetime import datetime, timedelta

from fastapi import APIRouter, HTTPException

from ..dao.dao import get_aggregated_stats, get_trend_stats
from ..schema.trend_analysis import (
    AggregatedStatsRes,
    IndivTrendStatsRes,
    TrendStatsRes,
)
from ..schema.user_filter import Filter

router = APIRouter(prefix="/trend-analysis", tags=["trend_analysis"])

# Declare MongoDB collection names to interact with
# FB_POSTS = os.getenv("DB_FACEBOOK_POSTS_COLLECTION")
# FB_COMMENTS = os.getenv("DB_FACEBOOK_COMMENTS_COLLECTION")
FB_POSTS = "facebook_posts_v1"
FB_COMMENTS = "facebook_comments_v1"
TWITTER_TWEETS = os.getenv("DB_TWIITER_TWEETS_COLLECTION")
TWITTER_COMMENTS = os.getenv("DB_TWITTER_COMMENTS_COLLECTION")
REDDIT_SUBMISSIONS = os.getenv("DB_REDDIT_SUBMISSIONS_COLLECTION")
REDDIT_COMMENTS = os.getenv("DB_REDDIT_COMMENTS_COLLECTION")
YOUTUBE_VIDEOS = os.getenv("DB_YOUTUBE_VIDEOS_COLLECTION")
YOUTUBE_COMMENTS = os.getenv("DB_YOUTUBE_COMMENTS_COLLECTION")


@router.post("/get-all-aggregated-stats", response_model=AggregatedStatsRes)
def get_all_aggregated_stats(filter: Filter):
    """
    To get aggregated statistics (total posts, total comments, total likes, percentage of posts per platform).

    Args:
        filter (Filter): JSON request body (user's filter options)

    Returns:
        Pydantic Model: JSON response object
    """

    # Query selected social media platform MongoDB collection based on user platform filter options
    if "facebook" in filter.platforms:
        fb_posts_data = get_aggregated_stats(filter, FB_POSTS)
        fb_comments_data = get_aggregated_stats(filter, FB_COMMENTS)
    else:
        fb_posts_data = fb_comments_data = {}
    if "twitter" in filter.platforms:
        twit_tweets_data = get_aggregated_stats(filter, TWITTER_TWEETS)
        twit_comments_data = get_aggregated_stats(filter, TWITTER_COMMENTS)
    else:
        twit_tweets_data = twit_comments_data = {}
    if "reddit" in filter.platforms:
        reddit_submissions_data = get_aggregated_stats(filter, REDDIT_SUBMISSIONS)
        reddit_comments_data = get_aggregated_stats(filter, REDDIT_COMMENTS)
    else:
        reddit_submissions_data = reddit_comments_data = {}
    # if "youtube" in filter.platforms:
    #     youtube_videos_data = get_aggregated_stats(filter, YOUTUBE_VIDEOS)
    #     youtube_comments_data = get_aggregated_stats(filter, YOUTUBE_COMMENTS)
    # else:
    #     youtube_videos_data = youtube_comments_data = {}

    # Create list of records from all social media platforms for posts and comments,
    all_posts = [
        fb_posts_data,
        twit_tweets_data,
        reddit_submissions_data,
        # youtube_videos_data
    ]
    all_comments = [
        fb_comments_data,
        twit_comments_data,
        reddit_comments_data,
        # youtube_comments_data,
    ]

    # Calc required statistics and metrics
    total_posts = sum(data.get("count", 0) for data in all_posts)
    total_comments = sum(data.get("count", 0) for data in all_comments)
    total_likes = sum(data.get("total_likes", 0) for data in all_posts) + sum(
        data.get("total_likes", 0) for data in all_comments
    )
    total_records = total_posts + total_comments

    platform_metrics = {
        "facebook": {
            "mentions": round(
                (fb_posts_data.get("count", 0) + fb_comments_data.get("count", 0)) / total_records,
                2,
            ),
            "emotion": get_top_emotion(fb_posts_data, fb_comments_data),
        },
        "twitter": {
            "mentions": round(
                (twit_tweets_data.get("count", 0) + twit_tweets_data.get("count", 0))
                / total_records,
                2,
            ),
            "emotion": get_top_emotion(twit_tweets_data, twit_comments_data),
        },
        "reddit": {
            "mentions": round(
                (reddit_submissions_data.get("count", 0) + reddit_comments_data.get("count", 0))
                / total_records,
                2,
            ),
            "emotion": get_top_emotion(reddit_submissions_data, reddit_comments_data),
        },
    }

    return {
        "posts": total_posts,
        "comments": total_comments,
        "likes": total_likes,
        "platformMetrics": platform_metrics,
    }


def get_top_emotion(posts_data, comments_data) -> str:
    """
    Util function to get the emotion label with the most count

    Args:
        posts_data (_type_): social media post data (post refers to posts, tweets, submissions, videos)
        comments_data (_type_): social media comments data

    Returns:
        str: emotion label
    """
    emotions_ls = posts_data.get("emotion_counts", []) + comments_data.get("emotion_counts", [])

    emotion_total_counts = {}
    for d in emotions_ls:
        emotion_total_counts[d["emotion"]] = emotion_total_counts.get(d["emotion"], 0) + d["count"]

    if emotion_total_counts:
        return max(emotion_total_counts, key=emotion_total_counts.get)
    else:
        return None


@router.post("/get-all-trend-stats", response_model=TrendStatsRes)
def get_all_trend_stats(filter: Filter):
    """
    To get the total trend percentage change between user's selected filter time period and the same period range before the selected time period.

    Args:
        filter (Filter): JSON request body (user's filter options)

    Returns:
        Pydantic Model: JSON response object
    """

    # Create a deep copy of user filter and change the endDate key value to the endDate of previous date range
    prev_date_filter = copy.deepcopy(filter)
    prev_end_date = datetime.strptime(filter.endDate, "%Y-%m-%d") - timedelta(days=filter.numDays)
    prev_date_filter.endDate = prev_end_date.strftime("%Y-%m-%d")

    # Query selected social media platform MongoDB collection based on user platform filter options
    if "facebook" in filter.platforms:
        fb_posts_count = get_trend_stats(filter, FB_POSTS)
        fb_comments_count = get_trend_stats(filter, FB_COMMENTS)
        fb_posts_count_prev = get_trend_stats(prev_date_filter, FB_POSTS)
        fb_comments_count_prev = get_trend_stats(prev_date_filter, FB_COMMENTS)
    else:
        fb_posts_count = fb_comments_count = fb_posts_count_prev = fb_comments_count_prev = 0
    if "twitter" in filter.platforms:
        twit_tweets_count = get_trend_stats(filter, TWITTER_TWEETS)
        twit_comments_count = get_trend_stats(filter, TWITTER_COMMENTS)
        twit_tweets_count_prev = get_trend_stats(prev_date_filter, TWITTER_TWEETS)
        twit_comments_count_prev = get_trend_stats(prev_date_filter, TWITTER_COMMENTS)
    else:
        twit_tweets_count = twit_comments_count = 0
        twit_tweets_count_prev = twit_comments_count_prev = 0
    if "reddit" in filter.platforms:
        reddit_submissions_count = get_trend_stats(filter, REDDIT_SUBMISSIONS)
        reddit_comments_count = get_trend_stats(filter, REDDIT_COMMENTS)
        reddit_submissions_count_prev = get_trend_stats(prev_date_filter, REDDIT_SUBMISSIONS)
        reddit_comments_count_prev = get_trend_stats(prev_date_filter, REDDIT_COMMENTS)
        print(reddit_submissions_count)
    else:
        reddit_submissions_count = reddit_comments_count = 0
        reddit_submissions_count_prev = reddit_comments_count_prev = 0
    # if "youtube" in filter.platforms:
    #     youtube_videos_count = get_trend_stats(filter, YOUTUBE_VIDEOS)
    #     youtube_comments_count = get_trend_stats(filter, YOUTUBE_COMMENTS)
    #     youtube_videos_count_prev = get_trend_stats(prev_date_filter, YOUTUBE_VIDEOS)
    #     youtube_comments_count_prev = get_trend_stats(prev_date_filter, YOUTUBE_COMMENTS)
    # else:
    #     youtube_videos_count = youtube_comments_count = 0
    #     youtube_videos_count_prev = youtube_comments_count_prev = 0

    # Calc total records for selected and previous date range
    selected_date_range_counts = sum(
        [
            fb_posts_count,
            fb_comments_count,
            twit_tweets_count,
            twit_comments_count,
            reddit_submissions_count,
            reddit_comments_count,
            # youtube_videos_count,
            # youtube_comments_count,
        ],
        0,
    )
    prev_date_range_counts = sum(
        [
            fb_posts_count_prev,
            fb_comments_count_prev,
            twit_tweets_count_prev,
            twit_comments_count_prev,
            reddit_submissions_count_prev,
            reddit_comments_count_prev,
            # youtube_videos_count_prev,
            # youtube_comments_count_prev,
        ],
        0,
    )
    if prev_date_range_counts == 0:
        raise HTTPException(
            status_code=404, detail="No data found from previous data range to compare trend"
        )

    return {"trend": round(selected_date_range_counts / prev_date_range_counts, 2)}


@router.post("/get-indiv-trend-stats", response_model=IndivTrendStatsRes)
def get_indiv_trend_stats(filter: Filter):
    """
    To get the trend percentage change between user's selected filter time period and the same period range before the selected time period for each individual platform.

    Args:
        filter (Filter): JSON request body (user's filter options)

    Returns:
        Pydantic Model: JSON response object
    """

    # Create a deep copy of user filter and change the endDate key value to the endDate of previous date range
    prev_date_filter = copy.deepcopy(filter)
    prev_end_date = datetime.strptime(filter.endDate, "%Y-%m-%d") - timedelta(days=filter.numDays)
    prev_date_filter.endDate = prev_end_date.strftime("%Y-%m-%d")

    # Query selected social media platform MongoDB collection based on user platform filter options
    if "facebook" in filter.platforms:
        fb_posts_count = get_trend_stats(filter, FB_POSTS)
        fb_comments_count = get_trend_stats(filter, FB_COMMENTS)
        fb_posts_count_prev = get_trend_stats(prev_date_filter, FB_POSTS)
        fb_comments_count_prev = get_trend_stats(prev_date_filter, FB_COMMENTS)
    else:
        fb_posts_count = fb_comments_count = fb_posts_count_prev = fb_comments_count_prev = 0
    if "twitter" in filter.platforms:
        twit_tweets_count = get_trend_stats(filter, TWITTER_TWEETS)
        twit_comments_count = get_trend_stats(filter, TWITTER_COMMENTS)
        twit_tweets_count_prev = get_trend_stats(prev_date_filter, TWITTER_TWEETS)
        twit_comments_count_prev = get_trend_stats(prev_date_filter, TWITTER_COMMENTS)
    else:
        twit_tweets_count = twit_comments_count = 0
        twit_tweets_count_prev = twit_comments_count_prev = 0
    if "reddit" in filter.platforms:
        reddit_submissions_count = get_trend_stats(filter, REDDIT_SUBMISSIONS)
        reddit_comments_count = get_trend_stats(filter, REDDIT_COMMENTS)
        reddit_submissions_count_prev = get_trend_stats(prev_date_filter, REDDIT_SUBMISSIONS)
        reddit_comments_count_prev = get_trend_stats(prev_date_filter, REDDIT_COMMENTS)
    else:
        reddit_submissions_count = reddit_comments_count = 0
        reddit_submissions_count_prev = reddit_comments_count_prev = 0
    # if "youtube" in filter.platforms:
    #     youtube_videos_count = get_trend_stats(filter, YOUTUBE_VIDEOS)
    #     youtube_comments_count = get_trend_stats(filter, YOUTUBE_COMMENTS)
    #     youtube_videos_count_prev = get_trend_stats(prev_date_filter, YOUTUBE_VIDEOS)
    #     youtube_comments_count_prev = get_trend_stats(prev_date_filter, YOUTUBE_COMMENTS)
    # else:
    #     youtube_videos_count = youtube_comments_count = 0
    #     youtube_videos_count_prev = youtube_comments_count_prev = 0

    return {
        "facebook": {
            "trend": get_trend_change(
                fb_posts_count, fb_comments_count, fb_posts_count_prev, fb_comments_count_prev
            )
        },
        "twitter": {
            "trend": get_trend_change(
                twit_tweets_count,
                twit_comments_count,
                twit_tweets_count_prev,
                twit_comments_count_prev,
            )
        },
        "reddit": {
            "trend": get_trend_change(
                reddit_submissions_count,
                reddit_comments_count,
                reddit_submissions_count_prev,
                reddit_comments_count_prev,
            )
        },
        # "youtube": {
        #     "trend": get_trend_change(
        #         youtube_videos_count,
        #         youtube_comments_count,
        #         youtube_videos_count_prev,
        #         youtube_comments_count_prev,
        #     )
        # },
    }


def get_trend_change(posts_count, comments_count, posts_count_prev, comments_count_prev) -> float:
    """
    Util func to calculate trend change for a social media platform.

    Args:
        posts_count (int): Selected date range posts count (post refers to posts, tweets, submissions, videos)
        comments_count (int): Selected date range comments count
        posts_count_prev (int): Previous date range posts count (post refers to posts, tweets, submissions, videos)
        comments_count_prev (int): Previous date range comments count

    Returns:
        float: trend change
    """
    if (posts_count_prev + comments_count_prev) == 0:
        return 0 if posts_count + comments_count == 0 else 1
    if (posts_count + comments_count) == 0:
        return 0
    return round((posts_count + comments_count) / (posts_count_prev + comments_count_prev), 2)
