import os
from typing import List

from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException

from ..database.connect import db
from ..schema.facebook import (
    FbComplaintTopKeywordsAnalysisRes,
    FbIndivAggregatedStatsRes,
    FbKeywordAnalysisRes,
    FbTop5TopicStatsRes,
)
from ..schema.user_filter import Filter
from .user_filter import db_filter_query_from_user_filter

router = APIRouter(prefix="/facebook", tags=["facebook"])

# Load environment variables
load_dotenv()

# Declare MongoDB collection names to interact with
# FB_POSTS = os.getenv("DB_FACEBOOK_POSTS_COLLECTION")
# FB_COMMENTS = os.getenv("DB_FACEBOOK_COMMENTS_COLLECTION")
FB_POSTS = "facebook_posts_v1"
FB_COMMENTS = "facebook_comments_v1"

@router.post("/get-top5-topics-stats", response_model=FbTop5TopicStatsRes)
def get_fb_top5_topics_stats(filter: Filter, project: dict, db_collection: str):
    """
    Query the db based on user filter and select only relevant fields for top 5 topic analysis.

    Args:
        filter (Filter): JSON request body (user's filter options)
        project (dict): MongoDB project field for query statement

    Returns:
        list: List of records
    """
    collection = FB_POSTS if db_collection == "posts" else FB_COMMENTS
    db_query = db_filter_query_from_user_filter(filter)

    return list(db[collection].find(db_query, project))


@router.post("/get-aggregated-stats", response_model=FbIndivAggregatedStatsRes)
def get_fb_aggregated_stats(filter: Filter, db_collection: str):
    """
    Query the db based on user filter and select only relevant fields for trend analysis (aggregated stats).

    Args:
        filter (Filter): JSON request body (user's filter options)

    Returns:
        dict: DB queried result
    """
    collection = FB_POSTS if db_collection == "posts" else FB_COMMENTS

    filter_query = db_filter_query_from_user_filter(filter)

    db_query = [
        {"$match": filter_query},
        {
            "$group": {
                "_id": None,
                "total_likes": {"$sum": "$likes_cnt"},
                "count": {"$sum": 1},
                "top_emotion": {"$first": "$emotions_label"},
            }
        },
        {"$project": {"total_likes": 1, "count": 1, "top_emotion": 1, "_id": False}},
    ]

    if not list(db[collection].aggregate(db_query)):
        return {}
        
    res = list(db[collection].aggregate(db_query))[0]
    res["emotion_counts"] = get_emotions_count(filter_query, collection)

    return res


def get_emotions_count(filter_query: dict, collection: str) -> list:
    db_query = [
        {"$match": filter_query},
        {"$unwind": "$emotions_label"},
        {"$group": {"_id": "$emotions_label", "count": {"$sum": 1}}},
        {"$project": {"emotion": "$_id", "count": 1, "_id": False}},
    ]

    return list(db[collection].aggregate(db_query))


@router.post("/get-trend-stats", response_model=int)
def get_fb_trend_stats(filter: Filter, db_collection: str):
    """
    Query the db based on user filter and get number of records.

    Args:
        filter (Filter): JSON request body (user's filter options)

    Returns:
        int: Number of documents/records
    """
    collection = FB_POSTS if db_collection == "posts" else FB_COMMENTS

    db_query = db_filter_query_from_user_filter(filter)

    return db[collection].count_documents(db_query)


@router.post("/get-top-keywords", response_model=List[FbKeywordAnalysisRes])
def get_top_keywords(filter: Filter, project: dict, db_collection: str):
    """
    Query the db based on user filter and get entities and sentiments

    Args:
        filter (Filter): JSON request body (user's filter options)
        project (dict): MongoDB project field for query statement

    Returns:
        list: List of records
    """
    collection = FB_POSTS if db_collection == "posts" else FB_COMMENTS

    db_query = db_filter_query_from_user_filter(filter)

    return list(db[collection].find(db_query, project))


@router.post("/get-top-complaint-keywords", response_model=List[FbComplaintTopKeywordsAnalysisRes])
def get_top_complaint_keywords(filter: Filter, project: dict, db_collection: str):
    """
    Query the db based on user filter to only get complaint records and their entities

    Args:
        filter (Filter): JSON request body (user's filter options)
        project (dict): MongoDB project field for query statement

    Returns:
        list: List of records
    """
    collection = FB_POSTS if db_collection == "posts" else FB_COMMENTS

    db_query = db_filter_query_from_user_filter(filter)
    db_query["intent"] = {"$regex": "complaint"}

    return list(db[collection].find(db_query, project))
