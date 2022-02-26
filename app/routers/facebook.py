from fastapi import APIRouter, Query, HTTPException
from ..database.connect import db
from ..schema.facebook import FbPostRes, FbDailyStatsRes
from typing import List
from datetime import datetime, timedelta

router = APIRouter(prefix="/facebook", tags=["facebook"])

# Declare MongoDB collection names to interact with
FB_POSTS = "fb_posts"
FB_COMMENTS = "fb_comments"


@router.get("/get-posts/", response_model=List[FbPostRes])
async def get_posts(
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
    posts = list(db.fb_posts.find(db_query))

    if len(posts) == 0:
        raise HTTPException(
            status_code=404,
            detail=f"No posts found within date period {start_date} to {end_date}",
        )

    return posts


@router.get("/get-daily-stats/", response_model=List[FbDailyStatsRes])
async def get_daily_stats(
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
        List[FbDailyStatsRes]: List of Pydantic response model
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
        {"$project": {"_id": 0}},
    ]
    stats = list(db.fb_posts.aggregate(db_query))

    if len(stats) == 0:
        raise HTTPException(
            status_code=404,
            detail=f"No data found within date period {start_date} to {end_date}",
        )

    return stats
