from datetime import datetime

from fastapi import APIRouter

from ..schema.trend_analysis import AggregatedStatsRes
from ..schema.user_filter import Filter
from .facebook import get_aggregated_stats

router = APIRouter(prefix="/trend-analysis", tags=["trend_analysis"])


@router.get("/get-all-aggregated-stats", response_model=AggregatedStatsRes)
def get_all_aggregated_stats(filter: Filter):
    """
    _summary_

    Args:
        filter (Filter): _description_

    Returns:
        _type_: _description_
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

    print(fb_data[0]['count'])
    print(fb_data1[0]['count'])

    total_posts = sum(data[0]["count"] for data in all_data)
    print(total_posts)
    total_likes = sum(data[0]["total_likes"] for data in all_data)

    platform_metrics = {
        "platform1": round(fb_data[0]['count'] / total_posts, 2),
        "platform2": round(fb_data1[0]['count'] / total_posts, 2),
    }

    return {"posts": total_posts, "likes": total_likes, "platformMetrics": platform_metrics}
