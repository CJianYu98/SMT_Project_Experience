from fastapi import APIRouter

from ..schema.trend_analysis import (
    AggregatedStatsRes,
    IndivTrendStatsRes,
    TrendStatsRes,
)
from ..schema.user_filter import Filter
from .facebook import get_fb_aggregated_stats, get_fb_trend_stats

router = APIRouter(prefix="/trend-analysis", tags=["trend_analysis"])


@router.post("/get-all-aggregated-stats", response_model=AggregatedStatsRes)
def get_all_aggregated_stats(filter: Filter):
    """
    To get aggregated statistics (total posts, total comments, total likes, percentage of posts per platform).

    Args:
        filter (Filter): JSON request body (user's filter options)

    Returns:
        Pydantic Model: JSON response object
    """

    def get_top_emotion(posts_data, comments_data) -> str:
        emotions_ls = posts_data["emotion_counts"] + comments_data["emotion_counts"]

        emotion_total_counts = {}
        for d in emotions_ls:
            emotion_total_counts[d["emotion"]] = (
                emotion_total_counts.get(d["emotion"], 0) + d["count"]
            )

        return max(emotion_total_counts, key=emotion_total_counts.get)

    if "facebook" in filter.platforms:
        fb_posts_data = get_fb_aggregated_stats(filter, "posts")
        fb_comments_data = get_fb_aggregated_stats(filter, "comments")
    else:
        fb_posts_data = fb_comments_data = []

    all_posts = [fb_posts_data]
    all_comments = [fb_comments_data]

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


@router.post("/get-all-trend-stats", response_model=TrendStatsRes)
def get_all_trend_stats(filter: Filter):
    """
    To get the total trend percentage change between user's selected filter time period and the same period range before the selected time period.

    Args:
        filter (Filter): JSON request body (user's filter options)

    Returns:
        Pydantic Model: JSON response object
    """
    filter1 = Filter(
        endDate="2019-03-01",
        numDays=14,
        platforms=["Facebook", "Reddit"],
        sentiments=["positive", "negative", "neutral"],
        emotions=["joy", "sadness", "neutral", "anger", "fear"],
        query=None,
    )

    fb_posts_data = get_fb_trend_stats(filter)
    fb_posts_data1 = get_fb_trend_stats(filter1)

    return {"trend": round(fb_posts_data / fb_posts_data1, 2)}


@router.post("/get-indiv-trend-stats", response_model=IndivTrendStatsRes)
def get_indiv_trend_stats(filter: Filter):
    """
    To get the trend percentage change between user's selected filter time period and the same period range before the selected time period for each individual platform.

    Args:
        filter (Filter): JSON request body (user's filter options)

    Returns:
        Pydantic Model: JSON response object
    """
    filter1 = Filter(
        start_date="2019-02-01",
        end_date="2019-03-01",
        platforms=["Facebook", "Reddit"],
        sentiments=["positive", "negative", "neutral"],
        emotions=["joy", "sadness", "neutral", "anger", "fear"],
        query=None,
    )

    fb_posts_data = get_fb_trend_stats(filter)
    fb_posts_data1 = get_fb_trend_stats(filter1)

    return {
        "Facebook": {"trend": round(fb_posts_data / fb_posts_data1, 2)},
        "Twitter": {"trend": round(fb_posts_data / fb_posts_data1, 2)},
        "Reddit": {"trend": round(fb_posts_data / fb_posts_data1, 2)},
        "Youtube": {"trend": round(fb_posts_data / fb_posts_data1, 2)},
    }
