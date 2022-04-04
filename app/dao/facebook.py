from dotenv import load_dotenv
from fastapi import HTTPException

from ..database.connect import db
from ..schema.dao import (
    ComplaintTopKeywordsAnalysisRes,
    AggregatedStatsRes,
    KeywordAnalysisRes,
    Top5ComplaintOrNoteworthyCommentsRes,
    Top5TopicStatsRes,
    TrendStatsRes,
)
from ..schema.user_filter import Filter
from .user_filter import db_filter_query_from_user_filter

# Load environment variables
load_dotenv()

# Declare MongoDB collection names to interact with
# FB_POSTS = os.getenv("DB_FACEBOOK_POSTS_COLLECTION")
# FB_COMMENTS = os.getenv("DB_FACEBOOK_COMMENTS_COLLECTION")
FB_POSTS = "facebook_posts_v1"
FB_COMMENTS = "facebook_comments_v1"


def get_fb_top5_topics_stats(filter: Filter, db_collection: str):
    """
    Query the db based on user filter and select only relevant fields for top 5 topic analysis.

    Args:
        filter (Filter): JSON request body (user's filter options)
        project (dict): MongoDB project field for query statement
        db_collection (str): To determine which collection to query from

    Raises:
        HTTPException: For data type error, using pydantic

    Returns:
        list: List of records
    """
    project = {
        "entities": 1,
        "emotions_label": 1,
        "sentiment_label": 1,
        "topic": 1,
        "text": "$message",
        "_id": False,
    }

    collection = FB_POSTS if db_collection == "posts" else FB_COMMENTS
    db_query = db_filter_query_from_user_filter(filter)

    res = list(db[collection].find(db_query, project))

    try:
        Top5TopicStatsRes(data=res)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e

    return res


def get_fb_aggregated_stats(filter: Filter, db_collection: str):
    """
    Query the db based on user filter and select only relevant fields for trend analysis (aggregated stats).

    Args:
        filter (Filter): JSON request body (user's filter options)
        db_collection (str): To determine which collection to query from

    Raises:
        HTTPException: For data type error, using pydantic

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

    try:
        AggregatedStatsRes(
            total_likes=res["total_likes"], count=res["count"], emotion_counts=res["emotion_counts"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e

    return res


def get_emotions_count(filter_query: dict, collection: str) -> list:
    """
    Get the counts for each emotion

    Args:
        filter_query (dict): _description_
        collection (str): _description_

    Raises:
        HTTPException: For data type error, using pydantic

    Returns:
        list: _description_
    """
    db_query = [
        {"$match": filter_query},
        {"$unwind": "$emotions_label"},
        {"$group": {"_id": "$emotions_label", "count": {"$sum": 1}}},
        {"$project": {"emotion": "$_id", "count": 1, "_id": False}},
    ]

    return list(db[collection].aggregate(db_query))


def get_fb_trend_stats(filter: Filter, db_collection: str):
    """
    Query the db based on user filter and get number of records.

    Args:
        filter (Filter): JSON request body (user's filter options)
        db_collection (str): To determine which collection to query from

    Raises:
        HTTPException: For data type error, using pydantic

    Returns:
        int: Number of documents/records
    """
    collection = FB_POSTS if db_collection == "posts" else FB_COMMENTS
    db_query = db_filter_query_from_user_filter(filter)

    res = db[collection].count_documents(db_query)

    try:
        TrendStatsRes(count=res)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e

    return res


def get_fb_top_keywords(filter: Filter, project: dict, db_collection: str):
    """
    Query the db based on user filter and get entities and sentiments

    Args:
        filter (Filter): JSON request body (user's filter options)
        project (dict): MongoDB project field for query statement
        db_collection (str): To determine which collection to query from

    Raises:
        HTTPException: For data type error, using pydantic

    Returns:
        list: List of records
    """
    collection = FB_POSTS if db_collection == "posts" else FB_COMMENTS
    db_query = db_filter_query_from_user_filter(filter)

    res = list(db[collection].find(db_query, project))

    try:
        KeywordAnalysisRes(data=res)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e

    return res


def get_fb_top_complaint_keywords(filter: Filter, project: dict, db_collection: str):
    """
    Query the db based on user filter to only get complaint records and their entities

    Args:
        filter (Filter): JSON request body (user's filter options)
        project (dict): MongoDB project field for query statement
        db_collection (str): To determine which collection to query from

    Raises:
        HTTPException: For data type error, using pydantic

    Returns:
        list: List of records
    """
    collection = FB_POSTS if db_collection == "posts" else FB_COMMENTS
    db_query = db_filter_query_from_user_filter(filter)
    db_query["intent"] = {"$regex": "complaint"}

    res = list(db[collection].find(db_query, project))

    try:
        ComplaintTopKeywordsAnalysisRes(data=res)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e

    return res


def get_fb_top5_complaint_comments(filter: Filter):
    """
    Query the db based on user filter to get top 5 complaint related comments based on likes

    Args:
        filter (Filter): JSON request body (user's filter options)

    Raises:
        HTTPException: For data type error, using pydantic

    Returns:
        list: List of records(sorted by likes and dates)
    """
    project = {
        "likes": "$likes_cnt",
        "datetime": "$created_time",
        "comment": "$message",
        "topic": 1,
        "sentiment": "$sentiment_label",
        "emotion": "$emotions_label",
        "_id": False,
    }

    db_query = db_filter_query_from_user_filter(filter)
    db_query["intent"] = {"$regex": "complaint"}

    res_sort_by_likes = list(db[FB_COMMENTS].find(db_query, project).sort("likes_cnt", -1).limit(5))
    res_sort_by_date = list(
        db[FB_COMMENTS].find(db_query, project).sort("created_time", -1).limit(5)
    )

    try:
        Top5ComplaintOrNoteworthyCommentsRes(data=res_sort_by_likes)
        Top5ComplaintOrNoteworthyCommentsRes(data=res_sort_by_date)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e

    return res_sort_by_likes, res_sort_by_date


def get_top5_noteworthy_comments(filter: Filter):
    """
    Query the db based on user filter to get top 5 noteworthy related comments based on likes

    Args:
        filter (Filter): JSON request body (user's filter options)

    Raises:
        HTTPException: For data type error, using pydantic

    Returns:
        list: List of records(sorted by likes and dates)
    """
    project = {
        "likes": "$likes_cnt",
        "datetime": "$created_time",
        "comment": "$message",
        "topic": 1,
        "sentiment": "$sentiment_label",
        "emotion": "$emotions_label",
        "_id": False,
    }

    db_query = db_filter_query_from_user_filter(filter)
    db_query["isNoteworthy"] = 1

    res_sort_by_likes = list(db[FB_COMMENTS].find(db_query, project).sort("likes_cnt", -1).limit(5))
    res_sort_by_date = list(
        db[FB_COMMENTS].find(db_query, project).sort("created_time", -1).limit(5)
    )

    try:
        Top5ComplaintOrNoteworthyCommentsRes(data=res_sort_by_likes)
        Top5ComplaintOrNoteworthyCommentsRes(data=res_sort_by_date)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e

    return res_sort_by_likes, res_sort_by_date
