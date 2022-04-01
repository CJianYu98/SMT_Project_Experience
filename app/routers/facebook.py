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


@router.get("/get-posts", response_model=List[FbPostRes])
def get_posts(
    start_date: str = Query(..., regex="\d\d\d\d-\d\d-\d\d"),
    end_date: str = Query(..., regex="\d\d\d\d-\d\d-\d\d"),
):
    """
    Get all Facebook posts within a date range. To add one more day to the end_date argument in order to include data within that date.

    Args:
        start_date (str): Start date of the date range (Inclusive). Defaults to Query(..., regex="\d\d\d\d-\d\d-\d\d").
        end_date (str): End date of the date range (Exclusive). Defaults to Query(..., regex="\d\d\d\d-\d\d-\d\d").

    Raises:
        HTTPException: Raised when no Facebook posts found in the given date range

    Returns:
        List[FbPostRes]: List of Pydantic response model
    """
    start_date = datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.strptime(end_date, "%Y-%m-%d") + timedelta(days=1)

    db_query = {"created_time": {"$gte": start_date, "$lte": end_date}}
    posts = list(db[FB_POSTS].find(db_query))

    if not posts:
        raise HTTPException(
            status_code=404,
            detail=f"No posts found within date period {start_date} to {end_date}",
        )

    return posts


@router.get("/get-daily-stats", response_model=List[FbStatsRes])
def get_daily_stats(
    start_date: str = Query(..., regex="\d\d\d\d-\d\d-\d\d"),
    end_date: str = Query(..., regex="\d\d\d\d-\d\d-\d\d"),
):
    """
    Get Facebook daily statistics within a date range. To add one more day to the end_date argument in order to include data within that date.

    Args:
        start_date (str): Start date of the date range (Inclusive). Defaults to Query(..., regex="\d\d\d\d-\d\d-\d\d").
        end_date (str): End date of the date range (Exclusive). Defaults to Query(..., regex="\d\d\d\d-\d\d-\d\d").

    Raises:
        HTTPException: Raised when no Facebook data found in the given date range

    Returns:
        List[FbStatsRes]: List of Pydantic response model
    """
    start_date = datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.strptime(end_date, "%Y-%m-%d") + timedelta(days=1)

    db_query = [
        {"$match": {"created_time": {"$gte": start_date, "$lte": end_date}}},
        {
            "$group": {
                "_id": {
                    "year": {"$year": "$created_time"},
                    "month": {"$month": "$created_time"},
                    "day": {"$dayOfMonth": "$created_time"},
                },
                "total_comments": {"$sum": "$comments_cnt"},
                "total_likes": {"$sum": "$likes_cnt"},
                "count": {"$sum": 1},
            }
        },
        {"$addFields": {"date": "$_id"}},
        {"$project": {"_id": False}},
        {"$sort": {"date": 1}},
    ]
    stats = list(db[FB_POSTS].aggregate(db_query))

    if not stats:
        raise HTTPException(
            status_code=404,
            detail=f"No data found within date period {start_date} to {end_date}",
        )

    return stats


@router.get("/get-hourly-stats", response_model=List[FbStatsRes])
def get_hourly_stats(
    start_date: str = Query(..., regex="\d\d\d\d-\d\d-\d\d"),
    end_date: str = Query(..., regex="\d\d\d\d-\d\d-\d\d"),
):
    """
    Get Facebook hourly statistics within a date range. To add one more day to the end_date argument in order to include data within that date.

    Args:
        start_date (str): Start date of the date range (Inclusive). Defaults to Query(..., regex="\d\d\d\d-\d\d-\d\d").
        end_date (str): End date of the date range (Exclusive). Defaults to Query(..., regex="\d\d\d\d-\d\d-\d\d").

    Raises:
        HTTPException: Raised when no Facebook data found in the given date range

    Returns:
        List[FbStatsRes]: List of Pydantic response model
    """
    start_date = datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.strptime(end_date, "%Y-%m-%d") + timedelta(days=1)

    db_query = [
        {"$match": {"created_time": {"$gte": start_date, "$lte": end_date}}},
        {
            "$group": {
                "_id": {
                    "year": {"$year": "$created_time"},
                    "month": {"$month": "$created_time"},
                    "day": {"$dayOfMonth": "$created_time"},
                    "hour": {"$hour": "$created_time"},
                },
                "total_comments": {"$sum": "$comments_cnt"},
                "total_likes": {"$sum": "$likes_cnt"},
                "count": {"$sum": 1},
            }
        },
        {"$addFields": {"date": "$_id"}},
        {"$project": {"_id": False}},
        {"$sort": {"date": 1}},
    ]
    stats = list(db[FB_POSTS].aggregate(db_query))

    if not stats:
        raise HTTPException(
            status_code=404,
            detail=f"No data found within date period {start_date} to {end_date}",
        )

    return stats


@router.get("/get-trend/{num_days}", response_model=FbTrendRes)
def get_trend(
    start_date: str = Query(..., regex="\d\d\d\d-\d\d-\d\d"),
    end_date: str = Query(..., regex="\d\d\d\d-\d\d-\d\d"),
    num_days: int = Path(..., ge=1),
):
    """
    Get trend change (number of posts) between the given date range and the period num_days ago. To add one more day to the end_date argument in order to include data within that date.

    Args:
        start_date (str): Start date of the date range (Inclusive). Defaults to Query(..., regex="\d\d\d\d-\d\d-\d\d").
        end_date (str): End date of the date range (Exclusive). Defaults to Query(..., regex="\d\d\d\d-\d\d-\d\d").

    Raises:
        HTTPException: Raised when no Facebook data found in the given date range

    Returns:
        List[]: List of Pydantic response model
    """

    # Get stats for first date range
    start_date1 = datetime.strptime(start_date, "%Y-%m-%d")
    end_date1 = datetime.strptime(end_date, "%Y-%m-%d") + timedelta(days=1)

    db_query1 = [
        {"$match": {"created_time": {"$gte": start_date1, "$lte": end_date1}}},
        {
            "$group": {
                "_id": None,
                "total_comments": {"$sum": "$comments_cnt"},
                "total_likes": {"$sum": "$likes_cnt"},
                "count": {"$sum": 1},
            }
        },
        {"$project": {"_id": False}},
    ]
    stats1 = list(db[FB_POSTS].aggregate(db_query1))

    if not stats1:
        raise HTTPException(
            status_code=404,
            detail=f"No data found within date period 1 from {start_date1} to {end_date1}",
        )

    # Get stats for second date range
    end_date2 = start_date1 - timedelta(days=1)
    start_date2 = end_date2 - timedelta(days=num_days)

    db_query2 = [
        {"$match": {"created_time": {"$gte": start_date2, "$lte": end_date2}}},
        {
            "$group": {
                "_id": None,
                "total_comments": {"$sum": "$comments_cnt"},
                "total_likes": {"$sum": "$likes_cnt"},
                "count": {"$sum": 1},
            }
        },
        {"$project": {"_id": False}},
    ]
    stats2 = list(db[FB_POSTS].aggregate(db_query2))

    if not stats2:
        raise HTTPException(
            status_code=404,
            detail=f"No data found within date period 2 from {start_date2} to {end_date2}",
        )

    # Calculate trend percentage change between 2 periods
    perc_change = (stats1[0]["count"] / stats2[0]["count"]) - 1

    return {"perc_change": perc_change}


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
