from datetime import datetime

from fastapi import APIRouter

from ..schema.trend_analysis import AggregatedStatsRes
from ..schema.user_filter import Filter
from .facebook import get_aggregated_stats

router = APIRouter(prefix="/trend-analysis", tags=["trend_analysis"])


@router.get("/get-all-aggregated-stats", response_model=AggregatedStatsRes)
def get_all_aggregated_stats(filter: Filter):
    """
    To get aggregated statistics (total posts, total comments, total likes, percentage of posts per platform).

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

    fb_data = get_aggregated_stats(filter)
    fb_data1 = get_aggregated_stats(filter1)

    all_data = [fb_data, fb_data1]

    total_posts = sum(data[0]["count"] for data in all_data)
    total_likes = sum(data[0]["total_likes"] for data in all_data)

    platform_metrics = {
        "platform1": round(fb_data[0]['count'] / total_posts, 2),
        "platform2": round(fb_data1[0]['count'] / total_posts, 2),
    }

    return {"posts": total_posts, "likes": total_likes, "platformMetrics": platform_metrics}
