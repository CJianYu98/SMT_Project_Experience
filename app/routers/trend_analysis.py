import copy
import itertools
import os
from datetime import datetime, timedelta

from fastapi import APIRouter, HTTPException

from ..dao.dao import (
    get_aggregated_stats,
    get_social_media_feed_stats,
    get_trend_plot_data,
    get_trend_stats,
)
from ..schema.trend_analysis import (
    AggregatedStatsRes,
    IndivTrendStatsRes,
    SocialMediaFeedAggregatedStatsRes,
    TrendPlotDataRes,
    TrendStatsRes,
)
from ..schema.user_filter import Filter

router = APIRouter(prefix="/trend-analysis", tags=["trend_analysis"])

# Declare MongoDB collection names to interact with
FB_POSTS = os.getenv("DB_FACEBOOK_POSTS_COLLECTION")
FB_COMMENTS = os.getenv("DB_FACEBOOK_COMMENTS_COLLECTION")
TWITTER_TWEETS = os.getenv("DB_TWIITER_TWEETS_COLLECTION")
TWITTER_COMMENTS = os.getenv("DB_TWITTER_COMMENTS_COLLECTION")
REDDIT_SUBMISSIONS = os.getenv("DB_REDDIT_SUBMISSIONS_COLLECTION")
REDDIT_COMMENTS = os.getenv("DB_REDDIT_COMMENTS_COLLECTION")
YOUTUBE_VIDEOS = os.getenv("DB_YOUTUBE_VIDEOS_COLLECTION")
YOUTUBE_COMMENTS = os.getenv("DB_YOUTUBE_COMMENTS_COLLECTION")


@router.post(
    "/get-all-aggregated-stats",
    response_model=AggregatedStatsRes,
    response_model_exclude_none=True,
)
def get_all_aggregated_stats(filter: Filter):
    """
    To get aggregated statistics (total posts, total comments, total likes, percentage of posts per platform).

    Args:
        filter (Filter): JSON request body (user's filter options)

    Returns:
        Pydantic Model: JSON response object
    """

    all_posts = []
    all_comments = []
    platform_metrics = {}

    # Query selected social media platform MongoDB collection based on user platform filter options
    if "facebook" in filter.platforms:
        fb_posts_data = get_aggregated_stats(filter, FB_POSTS)
        fb_comments_data = get_aggregated_stats(filter, FB_COMMENTS)
        all_posts.append(fb_posts_data)
        all_comments.append(fb_comments_data)
        platform_metrics["facebook"] = {"emotion": get_top_emotion(fb_posts_data, fb_comments_data)}
    else:
        platform_metrics["facebook"] = None
    if "twitter" in filter.platforms:
        twit_tweets_data = get_aggregated_stats(filter, TWITTER_TWEETS)
        twit_comments_data = get_aggregated_stats(filter, TWITTER_COMMENTS)
        all_posts.append(twit_tweets_data)
        all_comments.append(twit_comments_data)
        platform_metrics["twitter"] = {
            "emotion": get_top_emotion(twit_tweets_data, twit_comments_data)
        }
    else:
        platform_metrics["twitter"] = None
    if "reddit" in filter.platforms:
        reddit_submissions_data = get_aggregated_stats(filter, REDDIT_SUBMISSIONS)
        reddit_comments_data = get_aggregated_stats(filter, REDDIT_COMMENTS)
        all_posts.append(reddit_submissions_data)
        all_comments.append(reddit_comments_data)
        platform_metrics["reddit"] = {
            "emotion": get_top_emotion(reddit_submissions_data, reddit_comments_data)
        }
    else:
        platform_metrics["reddit"] = None
    if "youtube" in filter.platforms:
        youtube_videos_data = get_aggregated_stats(filter, YOUTUBE_VIDEOS)
        youtube_comments_data = get_aggregated_stats(filter, YOUTUBE_COMMENTS)
        all_posts.append(youtube_videos_data)
        all_comments.append(youtube_comments_data)
        platform_metrics["youtube"] = {
            "emotion": get_top_emotion(youtube_videos_data, youtube_comments_data)
        }
    else:
        platform_metrics["youtube"] = None

    # Calc required statistics and metrics
    total_posts = sum(data.get("count", 0) for data in all_posts)
    total_comments = sum(data.get("count", 0) for data in all_comments)
    total_likes = sum(data.get("total_likes", 0) for data in all_posts) + sum(
        data.get("total_likes", 0) for data in all_comments
    )
    total_records = total_posts + total_comments

    if total_records != 0:
        if "facebook" in filter.platforms:
            platform_metrics["facebook"]["mentions"] = round(
                (fb_posts_data.get("count", 0) + fb_comments_data.get("count", 0)) / total_records,
                2,
            )
        if "twitter" in filter.platforms:
            platform_metrics["twitter"]["mentions"] = round(
                (twit_tweets_data.get("count", 0) + twit_comments_data.get("count", 0))
                / total_records,
                2,
            )
        if "reddit" in filter.platforms:
            platform_metrics["reddit"]["mentions"] = round(
                (reddit_submissions_data.get("count", 0) + reddit_comments_data.get("count", 0))
                / total_records,
                2,
            )
        if "youtube" in filter.platforms:
            platform_metrics["youtube"]["mentions"] = round(
                (youtube_videos_data.get("count", 0) + youtube_comments_data.get("count", 0))
                / total_records,
                2,
            )

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
    else:
        reddit_submissions_count = reddit_comments_count = 0
        reddit_submissions_count_prev = reddit_comments_count_prev = 0
    if "youtube" in filter.platforms:
        youtube_videos_count = get_trend_stats(filter, YOUTUBE_VIDEOS)
        youtube_comments_count = get_trend_stats(filter, YOUTUBE_COMMENTS)
        youtube_videos_count_prev = get_trend_stats(prev_date_filter, YOUTUBE_VIDEOS)
        youtube_comments_count_prev = get_trend_stats(prev_date_filter, YOUTUBE_COMMENTS)
    else:
        youtube_videos_count = youtube_comments_count = 0
        youtube_videos_count_prev = youtube_comments_count_prev = 0

    # Calc total records for selected and previous date range
    selected_date_range_counts = sum(
        [
            fb_posts_count,
            fb_comments_count,
            twit_tweets_count,
            twit_comments_count,
            reddit_submissions_count,
            reddit_comments_count,
            youtube_videos_count,
            youtube_comments_count,
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
            youtube_videos_count_prev,
            youtube_comments_count_prev,
        ],
        0,
    )
    if prev_date_range_counts == 0:
        raise HTTPException(
            status_code=404, detail="No data found from previous data range to compare trend"
        )

    return {"trend": round(selected_date_range_counts / prev_date_range_counts, 2)}


@router.post(
    "/get-indiv-trend-stats", response_model=IndivTrendStatsRes, response_model_exclude_none=True
)
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

    # Create response body
    res = {}

    # Query selected social media platform MongoDB collection based on user platform filter options
    if "facebook" in filter.platforms:
        res["facebook"] = {
            "trend": get_trend_change(
                get_trend_stats(filter, FB_POSTS),
                get_trend_stats(filter, FB_COMMENTS),
                get_trend_stats(prev_date_filter, FB_POSTS),
                get_trend_stats(prev_date_filter, FB_COMMENTS),
            )
        }

    if "twitter" in filter.platforms:
        res["twitter"] = {
            "trend": get_trend_change(
                get_trend_stats(filter, TWITTER_TWEETS),
                get_trend_stats(filter, TWITTER_COMMENTS),
                get_trend_stats(prev_date_filter, TWITTER_TWEETS),
                get_trend_stats(prev_date_filter, TWITTER_COMMENTS),
            )
        }

    if "reddit" in filter.platforms:
        res["reddit"] = {
            "trend": get_trend_change(
                get_trend_stats(filter, REDDIT_SUBMISSIONS),
                get_trend_stats(filter, REDDIT_COMMENTS),
                get_trend_stats(prev_date_filter, REDDIT_SUBMISSIONS),
                get_trend_stats(prev_date_filter, REDDIT_COMMENTS),
            )
        }

    if "youtube" in filter.platforms:
        res["youtube"] = {
            "trend": get_trend_change(
                get_trend_stats(filter, YOUTUBE_VIDEOS),
                get_trend_stats(filter, YOUTUBE_COMMENTS),
                get_trend_stats(prev_date_filter, YOUTUBE_VIDEOS),
                get_trend_stats(prev_date_filter, YOUTUBE_COMMENTS),
            )
        }

    return res


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


@router.post("/get-all-trend-plot-data", response_model=TrendPlotDataRes)
def get_all_trend_plot_data(filter: Filter):
    """
    To get trend plot data based on user's selected filter time period

    Args:
        filter (Filter): JSON request body (user's filter options)

    Returns:
        Pydantic Model: JSON response object
    """

    # Retrive and aggregate facebook trend plot data
    fb_posts_data = get_trend_plot_data(filter, FB_POSTS)
    fb_comments_data = get_trend_plot_data(filter, FB_COMMENTS)
    facebook_res = aggregate_platform_trend_data("facebook", fb_posts_data, fb_comments_data)

    # Retrive and aggregate reddit trend plot data
    reddit_submission_data = get_trend_plot_data(filter, REDDIT_SUBMISSIONS)
    reddit_comments_data = get_trend_plot_data(filter, REDDIT_COMMENTS)
    reddit_res = aggregate_platform_trend_data(
        "reddit", reddit_submission_data, reddit_comments_data
    )

    # Retrive and aggregate twiiter trend plot data
    twitter_tweets_data = get_trend_plot_data(filter, TWITTER_TWEETS)
    twitter_comments_data = get_trend_plot_data(filter, TWITTER_COMMENTS)
    twitter_res = aggregate_platform_trend_data(
        "twitter", twitter_tweets_data, twitter_comments_data
    )

    # Retrive and aggregate youtube trend plot data
    youtube_videos_data = get_trend_plot_data(filter, YOUTUBE_VIDEOS)
    youtube_comments_data = get_trend_plot_data(filter, YOUTUBE_COMMENTS)
    youtube_res = aggregate_platform_trend_data(
        "youtube", youtube_videos_data, youtube_comments_data
    )

    return {
        "facebook": facebook_res,
        "reddit": reddit_res,
        "twitter": twitter_res,
        "youtube": youtube_res,
    }


def aggregate_platform_trend_data(platform: str, posts_data: dict, comments_data: dict) -> dict:
    """
    Util func to aggregate trend plot data for a social media platform

    Args:
        platform (str): social media platform
        posts_data (dict): posts data (post refers to posts, tweets, submissions, videos)
        comments_data (dict): comments data

    Returns:
        dict: aggregated trend plot data
    """

    # Initialize res output variable
    res = {
        "dates": [],
        "mentions": [],
        "likes": [],
        "sentiments": {"positive": [], "neutral": [], "negative": []},
        "emotions": {"anger": [], "fear": [], "joy": [], "sadness": [], "neutral": []},
    }
    if platform == "reddit":
        res["awards"] = []
    elif platform == "twitter":
        res["retweets"] = []
    elif platform == "youtube":
        res["views"] = []

    # return if no posts/comments data
    if posts_data == [] and comments_data == []:
        return res

    # fields to aggregate
    output_fields = ["mentions", "likes", "sentiments", "emotions"]
    sentiments = ["positive", "neutral", "negative"]
    emotions = ["anger", "fear", "joy", "sadness", "neutral"]

    # Aggregate data, if no comments, then only aggregate posts data
    if posts_data and comments_data:
        for i, field in itertools.product(range(len(posts_data)), output_fields):
            if field == "sentiments":
                for sentiment in sentiments:
                    res[field][sentiment].append(
                        posts_data[i].get(f"{sentiment}_sentiment", 0)
                        + comments_data[i].get(f"{sentiment}_sentiment", 0)
                    )
            elif field == "emotions":
                for emotion in emotions:
                    res[field][emotion].append(
                        posts_data[i].get(f"{emotion}_emotion", 0)
                        + comments_data[i].get(f"{emotion}_emotion", 0)
                    )
            else:
                res[field].append(posts_data[i].get(field, 0) + comments_data[i].get(field, 0))
        
        for i in range(len(posts_data)):
            res["dates"].append(posts_data[i].get("date").strftime("%Y-%m-%d"))

            if platform == "reddit":
                res["awards"].append(
                    posts_data[i].get("awards", 0) + comments_data[i].get("awards", 0)
                )
            elif platform == "twitter":
                res["retweets"].append(
                    posts_data[i].get("retweets", 0) + comments_data[i].get("retweets", 0)
                )
            elif platform == "youtube":
                res["views"].append(posts_data[i].get("views", 0))
    elif posts_data:
        for i, field in itertools.product(range(len(posts_data)), output_fields):
            if field == "sentiments":
                for sentiment in sentiments:
                    res[field][sentiment].append(posts_data[i].get(f"{sentiment}_sentiment", 0))
            elif field == "emotions":
                for emotion in emotions:
                    res[field][emotion].append(posts_data[i].get(f"{emotion}_emotion", 0))
            else:
                res[field].append(posts_data[i].get(field, 0))

        for i in range(len(posts_data)):
            res["dates"].append(posts_data[i].get("date").strftime("%Y-%m-%d"))

            if platform == "reddit":
                res["awards"].append(posts_data[i].get("awards", 0))
            elif platform == "twitter":
                res["retweets"].append(posts_data[i].get("retweets", 0))
            elif platform == "youtube":
                res["views"].append(posts_data[i].get("views", 0))

    return res


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
        "emotions": [],
    }

    sentiments = ["positive", "neutral", "negative"]
    emotions = ["anger", "fear", "joy", "sadness", "neutral"]

    for sentiment in sentiments:
        res["sentiment"].append(
            {
                "sentiment": sentiment,
                "count": posts_data.get(f"{sentiment}_sentiment", 0)
                + comments_data.get(f"{sentiment}_sentiment", 0),
            }
        )

    for emotion in emotions:
        res["emotions"].append(
            {
                "emotion": emotion,
                "count": posts_data.get(f"{emotion}_emotion", 0)
                + comments_data.get(f"{emotion}_emotion", 0),
            }
        )

    return res


@router.post(
    "/get-social-media-aggregated-stats",
    response_model=SocialMediaFeedAggregatedStatsRes,
    response_model_exclude_none=True,
)
def get_social_media_aggregated_stats(filter: Filter):
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
        res["facebook"] = calc_aggregated_stats(fb_posts_data, fb_comments_data)
    if "twitter" in filter.platforms:
        twit_tweets_data = get_social_media_feed_stats(filter, TWITTER_TWEETS)
        twit_comments_data = get_social_media_feed_stats(filter, TWITTER_COMMENTS)
        res["twitter"] = calc_aggregated_stats(twit_tweets_data, twit_comments_data)
    if "reddit" in filter.platforms:
        reddit_submissions_data = get_social_media_feed_stats(filter, REDDIT_SUBMISSIONS)
        reddit_comments_data = get_social_media_feed_stats(filter, REDDIT_COMMENTS)
        res["reddit"] = calc_aggregated_stats(reddit_submissions_data, reddit_comments_data)
    if "youtube" in filter.platforms:
        youtube_videos_data = get_social_media_feed_stats(filter, YOUTUBE_VIDEOS)
        youtube_comments_data = get_social_media_feed_stats(filter, YOUTUBE_COMMENTS)
        res["youtube"] = calc_aggregated_stats(youtube_videos_data, youtube_comments_data)

    return res
