from datetime import datetime, timedelta
from typing import List

from fastapi import APIRouter, HTTPException, Path, Query

from ..database.connect import db
from ..schema.facebook import (
    FbAggregatedStatsRes,
    FbPostRes,
    FbStatsRes,
    FbTop5TopicStatsRes,
    FbTrendRes,
)
from ..schema.user_filter import Filter
from .user_filter import db_filter_query_from_user_filter

router = APIRouter(prefix="/facebook", tags=["facebook"])

# Declare MongoDB collection names to interact with
FB_POSTS = "fb_posts"
FB_COMMENTS = "fb_comments"


@router.get("/get-top5-topics-stats", response_model=FbTop5TopicStatsRes)
def get_fb_top5_topics_stats(filter: Filter, project: dict):
    """
    Query the db based on user filter and select only relevant fields for top 5 topic analysis.

    Args:
        filter (Filter): JSON request body (user's filter options)
        project (dict): MongoDB project field for query statement

    Returns:
        list: List of records
    """
    db_query = db_filter_query_from_user_filter(filter)

    # data = list(db['FB_POSTS'].find(db_query, project))
    return list(db.jianyu_play_girls.find(db_query, project))


@router.get("/get-aggregated-stats", response_model=FbAggregatedStatsRes)
def get_fb_aggregated_stats(filter: Filter):
    """
    Query the db based on user filter and select only relevant fields for trend analysis (aggregated stats).

    Args:
        filter (Filter): JSON request body (user's filter options)

    Returns:
        list: List of records
    """
    filter_query = db_filter_query_from_user_filter(filter)

    db_query = [
        {"$match": filter_query},
        {"$group": {"_id": None, "total_likes": {"$sum": "$likes_cnt"}, "count": {"$sum": 1}}},
        {"$project": {"total_likes": 1, "count": 1, "_id": False}},
    ]

    return list(db.jianyu_play_girls.aggregate(db_query))


@router.get("/get-trend-stats", response_model=int)
def get_fb_trend_stats(filter: Filter):
    """
    Query the db based on user filter and get number of records.

    Args:
        filter (Filter): JSON request body (user's filter options)

    Returns:
        int: Number of documents/records
    """
    db_query = db_filter_query_from_user_filter(filter)

    return db.jianyu_play_girls.count_documents(db_query)
