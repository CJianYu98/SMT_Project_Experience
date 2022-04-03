import copy
from datetime import datetime, timedelta

from fastapi import APIRouter, HTTPException

from ..schema.trend_analysis import (
    AggregatedStatsRes,
    IndivTrendStatsRes,
    TrendStatsRes,
)
from ..schema.user_filter import Filter
from ..dao.facebook import get_fb_aggregated_stats, get_fb_trend_stats

router = APIRouter(prefix="/trend-analysis", tags=["trend_analysis"])


@router.post("/get-all-aggregated-stats", response_model=AggregatedStatsRes)
def get_all_aggregated_stats(filter: Filter):
    """c
    To get aggregated statistics (total posts, total comments, total likes, percentage of posts per platform).

    Args:
        filter (Filter): JSON request body (user's filter options)

    Returns:
        Pydantic Model: JSON response object
    """

    # Query selected social media platform MongoDB collection based on user platform filter options
    if "facebook" in filter.platforms:
        fb_posts_data = get_fb_aggregated_stats(filter, "posts")
        fb_comments_data = get_fb_aggregated_stats(filter, "comments")
    else:
        fb_posts_data = fb_comments_data = []

    # Create list of records from all social media platforms for posts and comments,
    all_posts = [fb_posts_data]
    all_comments = [fb_comments_data]

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
        }
    }

    return {
        "posts": total_posts,
        "comments": total_comments,
        "likes": total_likes,
        "platformMetrics": platform_metrics,
    }


def get_top_emotion(posts_data, comments_data) -> str:
    emotions_ls = posts_data["emotion_counts"] + comments_data["emotion_counts"]

    emotion_total_counts = {}
    for d in emotions_ls:
        emotion_total_counts[d["emotion"]] = emotion_total_counts.get(d["emotion"], 0) + d["count"]

    return max(emotion_total_counts, key=emotion_total_counts.get)


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
    prev_end_date = datetime.strptime(filter.endDate, "%Y-%m-%d") - timedelta(
        days=filter.numDays + 1
    )
    prev_date_filter.endDate = prev_end_date.strftime("%Y-%m-%d")

    # Query selected social media platform MongoDB collection based on user platform filter options
    if "facebook" in filter.platforms:
        fb_posts_count = get_fb_trend_stats(filter, "posts")
        fb_comments_count = get_fb_trend_stats(filter, "comments")
        fb_posts_count_prev = get_fb_trend_stats(prev_date_filter, "posts")
        fb_comments_count_prev = get_fb_trend_stats(prev_date_filter, "comments")
    else:
        fb_posts_count = fb_comments_count = []

    # Calc total records for selected and previous date range
    selected_date_range_counts = sum([fb_posts_count, fb_comments_count])
    prev_date_range_counts = sum([fb_posts_count_prev, fb_comments_count_prev])
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
    prev_end_date = datetime.strptime(filter.endDate, "%Y-%m-%d") - timedelta(
        days=filter.numDays + 1
    )
    prev_date_filter.endDate = prev_end_date.strftime("%Y-%m-%d")

    # Query selected social media platform MongoDB collection based on user platform filter options
    if "facebook" in filter.platforms:
        fb_posts_count = get_fb_trend_stats(filter, "posts")
        fb_comments_count = get_fb_trend_stats(filter, "comments")
        fb_posts_count_prev = get_fb_trend_stats(prev_date_filter, "posts")
        fb_comments_count_prev = get_fb_trend_stats(prev_date_filter, "comments")
    else:
        fb_posts_count = fb_comments_count = []

    return {
        "Facebook": {
            "trend": round(
                (fb_posts_count + fb_comments_count)
                / (fb_posts_count_prev + fb_comments_count_prev),
                2,
            )
        },
        "Twitter": {
            "trend": round(
                (fb_posts_count + fb_comments_count)
                / (fb_posts_count_prev + fb_comments_count_prev),
                2,
            )
        },
        "Reddit": {
            "trend": round(
                (fb_posts_count + fb_comments_count)
                / (fb_posts_count_prev + fb_comments_count_prev),
                2,
            )
        },
        "Youtube": {
            "trend": round(
                (fb_posts_count + fb_comments_count)
                / (fb_posts_count_prev + fb_comments_count_prev),
                2,
            )
        },
    }
