from fastapi import APIRouter, Query
from ..database.connect import db
from ..schema import facebook
from typing import List
from datetime import datetime, timedelta

router = APIRouter(
    prefix="/facebook",
    tags= ["facebook"]
)

# Declare MongoDB collection names to interact with
FB_POSTS = "fb_posts"
FB_COMMENTS = "fb_comments"


@router.get("/get-posts/", response_model=facebook.FbPostRes)
async def get_posts(
    start_date: str = Query(..., regex="\d\d\d\d-\d\d-\d\d"), 
    end_date: str = Query(..., regex="\d\d\d\d-\d\d-\d\d")
):
    """
    Get all Facebook posts within a date range. To add one more day to the end_date argument in order to include data within that date.

    Args:
        start_date (str): Start date of the date range (Inclusive). Defaults to Query(..., regex="\d\d\d\d-\d\d-\d\d").
        end_date (str): End date of the date range (Exclusive). Defaults to Query(..., regex="\d\d\d\d-\d\d-\d\d").

    Returns:
        facebook.FbPostRes: Pydantic response model
    """
    start_date =  datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.strptime(end_date, '%Y-%m-%d') + timedelta(days=1)

    db_query = {
        "created_time": {
            "$gte": start_date,
            "$lte": end_date
        }
    }

    posts = db.fb_posts.find(db_query)
    return {
        "code": 200,
        "datetime": datetime.now(),
        "data": list(posts)
    }





