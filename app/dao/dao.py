import os

from dotenv import load_dotenv
from fastapi import HTTPException

from ..database.connect import db
from ..schema.dao import (
    AggregatedStatsRes,
    ComplaintTopKeywordsAnalysisRes,
    KeywordAnalysisRes,
    Top5ComplaintOrNoteworthyPostsRes,
    Top5NoteworthyTopicsRes,
    Top5TopicStatsRes,
    TrendPlotDataRes,
    TrendStatsRes,
)
from ..schema.user_filter import Filter
from .user_filter import db_filter_query_from_user_filter
from .utils import get_emotions_count

# Load environment variables
load_dotenv()

# DB datetime str
FB_DATETIME_STR = "created_time"
TWIT_DATETIME_STR = "created_at"
REDDIT_DATETIME_STR = "created_datetime"
YT_DATETIME_STR = "datetime"


def get_top5_topics_stats(filter: Filter, db_collection: str):
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
        "_id": False,
    }

    if "facebook" in db_collection:
        db_query = db_filter_query_from_user_filter(filter, datetime_str=FB_DATETIME_STR)
        project["text"] = "$message"
    elif "twitter" in db_collection:
        db_query = db_filter_query_from_user_filter(filter, datetime_str=TWIT_DATETIME_STR)
        project["text"] = "$tweet"
    elif "reddit" in db_collection:
        db_query = db_filter_query_from_user_filter(filter, datetime_str=REDDIT_DATETIME_STR)
        project["text"] = "$title" if "submissions" in db_collection else "$body"
    elif "youtube" in db_collection:
        db_query = db_filter_query_from_user_filter(filter, datetime_str=YT_DATETIME_STR)
        project["text"] = "$combined_text" if "videos" in db_collection else "$comment"

    res = list(db[db_collection].find(db_query, project))

    try:
        Top5TopicStatsRes(data=res)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e

    return res


def get_aggregated_stats(filter: Filter, db_collection: str):
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

    if "facebook" in db_collection:
        filter_query = db_filter_query_from_user_filter(filter, datetime_str=FB_DATETIME_STR)
        likes_str = "likes_cnt"
    elif "twitter" in db_collection:
        filter_query = db_filter_query_from_user_filter(filter, datetime_str=TWIT_DATETIME_STR)
        likes_str = "likes_count"
    elif "reddit" in db_collection:
        filter_query = db_filter_query_from_user_filter(filter, datetime_str=REDDIT_DATETIME_STR)
        likes_str = "score"
    elif "youtube" in db_collection:
        filter_query = db_filter_query_from_user_filter(filter, datetime_str=YT_DATETIME_STR)
        likes_str = "likes"

    db_query = [
        {"$match": filter_query},
        {
            "$group": {
                "_id": None,
                "total_likes": {"$sum": f"${likes_str}"},
                "count": {"$sum": 1},
                "top_emotion": {"$first": "$emotions_label"},
            }
        },
        {"$project": {"total_likes": 1, "count": 1, "top_emotion": 1, "_id": False}},
    ]
    res = list(db[db_collection].aggregate(db_query))
    if not res:
        return {}

    res = res[0]
    res["emotion_counts"] = get_emotions_count(filter_query, db_collection)

    try:
        AggregatedStatsRes(
            total_likes=res["total_likes"], count=res["count"], emotion_counts=res["emotion_counts"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e

    return res


def get_trend_stats(filter: Filter, db_collection: str):
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
    if "facebook" in db_collection:
        db_query = db_filter_query_from_user_filter(filter, datetime_str=FB_DATETIME_STR)
    elif "twitter" in db_collection:
        db_query = db_filter_query_from_user_filter(filter, datetime_str=TWIT_DATETIME_STR)
    elif "reddit" in db_collection:
        db_query = db_filter_query_from_user_filter(filter, datetime_str=REDDIT_DATETIME_STR)
    elif "youtube" in db_collection:
        db_query = db_filter_query_from_user_filter(filter, datetime_str=YT_DATETIME_STR)

    res = db[db_collection].count_documents(db_query)

    try:
        TrendStatsRes(count=res)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e

    return res


def get_trend_plot_data(filter: Filter, db_collection: str):
    """
    Query db based on user filter and aggregate various stats based on interval date range. Eg. Given the selected range, aggregate stats by per week/month.

    Args:
        filter (Filter): JSON request body (user's filter options)
        db_collection (str): To determine which collection to query from

    Raises:
        HTTPException: For data type error, using pydantic

    Returns:
        list: List of records
    """
    # Set the interval data unit for MongoDb query
    if filter.interval == "3hours":
        date_trunc_unit = "hour"
    elif filter.interval == "daily":
        date_trunc_unit = "day"
    elif filter.interval == "montly":
        date_trunc_unit = "month"
    elif filter.interval == "weekly":
        date_trunc_unit = "week"
    elif filter.interval == "yearly":
        date_trunc_unit = "year"

    # Set the bin size for MongoDB query
    bin_size = 3 if filter.interval == "3hours" else 1

    # Initialize group_query and project subquery statements for MongoDB query
    group_query = {}
    project = {"_id": False, "date": "$_id", "likes": 1, "mentions": 1}

    # Add on standard query fields to group_qeury statement
    for sentiment_val in ["positive", "negative", "neutral"]:
        group_query[f"{sentiment_val}_sentiment"] = create_sentiment_emotion_aggregate_subquery(
            "sentiment_label", sentiment_val
        )
        project[f"{sentiment_val}_sentiment"] = 1
    for emotion_val in ["anger", "fear", "joy", "sadness", "neutral"]:
        group_query[f"{emotion_val}_emotion"] = create_sentiment_emotion_aggregate_subquery(
            "emotions_label", emotion_val
        )
        project[f"{emotion_val}_emotion"] = 1

    # Create query field variables based on social media platform
    if "facebook" in db_collection:
        datetime_str = FB_DATETIME_STR
        likes_str = "likes_cnt"
    elif "twitter" in db_collection:
        datetime_str = TWIT_DATETIME_STR
        likes_str = "likes_count"
        group_query["retweets"] = {"$sum": "retweets_count"}
        project["retweets"] = 1
    elif "reddit" in db_collection:
        datetime_str = REDDIT_DATETIME_STR
        likes_str = "score"
        group_query["awards"] = {"$sum": "total_awards_received"}
        project["awards"] = 1
    elif "youtube" in db_collection:
        datetime_str = YT_DATETIME_STR
        likes_str = "likes"
        if "videos" in db_collection:
            group_query["views"] = {"$sum": "views"}
            project["views"] = 1

    # Create match query statement for MongoDB query
    match_query = db_filter_query_from_user_filter(filter, datetime_str=datetime_str)

    # Add on to group query statement
    group_query["_id"] = {
        "$dateTrunc": {"date": f"${datetime_str}", "unit": date_trunc_unit, "binSize": bin_size}
    }
    group_query["mentions"] = {"$sum": 1}
    group_query["likes"] = {"$sum": f"${likes_str}"}

    # Create the db based on above created subquery statements
    res = list(
        db[db_collection].aggregate(
            [{"$match": match_query}, {"$group": group_query}, {"$project": project}]
        )
    )

    try:
        TrendPlotDataRes(data=res)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e

    return sorted(res, key=lambda x: x["date"])


def create_sentiment_emotion_aggregate_subquery(field: str, value: str):
    """
    Aggregate number of each sentiment/emotion type

    Args:
        field (str): emotion/sentiment MongoDB field
        value (str): the type of emotion/sentiment

    Returns:
        dict: subquery statement for MongoDB query
    """
    return {"$sum": {"$cond": [{"$regexMatch": {"input": f"${field}", "regex": value}}, 1, 0]}}


def get_top_keywords(filter: Filter, project: dict, db_collection: str):
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
    if "facebook" in db_collection:
        db_query = db_filter_query_from_user_filter(filter, datetime_str=FB_DATETIME_STR)
    elif "twitter" in db_collection:
        db_query = db_filter_query_from_user_filter(filter, datetime_str=TWIT_DATETIME_STR)
    elif "reddit" in db_collection:
        db_query = db_filter_query_from_user_filter(filter, datetime_str=REDDIT_DATETIME_STR)
    elif "youtube" in db_collection:
        db_query = db_filter_query_from_user_filter(filter, datetime_str=YT_DATETIME_STR)

    res = list(db[db_collection].find(db_query, project))

    try:
        KeywordAnalysisRes(data=res)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e

    return res


def get_top_complaint_keywords(filter: Filter, project: dict, db_collection: str):
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
    if "facebook" in db_collection:
        db_query = db_filter_query_from_user_filter(filter, datetime_str=FB_DATETIME_STR)
    elif "twitter" in db_collection:
        db_query = db_filter_query_from_user_filter(filter, datetime_str=TWIT_DATETIME_STR)
    elif "reddit" in db_collection:
        db_query = db_filter_query_from_user_filter(filter, datetime_str=REDDIT_DATETIME_STR)
    elif "youtube" in db_collection:
        db_query = db_filter_query_from_user_filter(filter, datetime_str=YT_DATETIME_STR)
    db_query["intent"] = {"$regex": "complaint"}

    res = list(db[db_collection].find(db_query, project))

    try:
        ComplaintTopKeywordsAnalysisRes(data=res)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e

    return res


def get_top5_complaint_posts(filter: Filter, db_collection: str):
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
        "topic": 1,
        "sentiment": "$sentiment_label",
        "emotion": "$emotions_label",
        "_id": False,
    }

    if "facebook" in db_collection:
        db_query = db_filter_query_from_user_filter(filter, datetime_str=FB_DATETIME_STR)
        likes_key = "likes_cnt"
        datetime_key = FB_DATETIME_STR
        project["comment"] = "$message"
    elif "twitter" in db_collection:
        db_query = db_filter_query_from_user_filter(filter, datetime_str=TWIT_DATETIME_STR)
        likes_key = "likes_count"
        datetime_key = TWIT_DATETIME_STR
        project["comment"] = "$tweet"
        project["link"] = "$link"
    elif "reddit" in db_collection:
        db_query = db_filter_query_from_user_filter(filter, datetime_str=REDDIT_DATETIME_STR)
        likes_key = "score"
        datetime_key = REDDIT_DATETIME_STR
        project["comment"] = "$title"
        project["link"] = "$url"
    elif "youtube" in db_collection:
        db_query = db_filter_query_from_user_filter(filter, datetime_str=REDDIT_DATETIME_STR)
        likes_key = "likes"
        datetime_key = YT_DATETIME_STR
        project["comment"] = "$combined_text"
        project['link'] = "$url"
    if "facebook" not in db_collection:
        project["thumbnail"] = "$thumbnail"
    project["likes"] = f"${likes_key}"
    project["datetime"] = f"${datetime_key}"

    db_query["intent"] = {"$regex": "complaint"}

    res_sort_by_likes = list(db[db_collection].find(db_query, project).sort(likes_key, -1).limit(filter.topN))
    res_sort_by_date = list(
        db[db_collection].find(db_query, project).sort(datetime_key, -1).limit(filter.topN)
    )

    try:
        Top5ComplaintOrNoteworthyPostsRes(data=res_sort_by_likes)
        Top5ComplaintOrNoteworthyPostsRes(data=res_sort_by_date)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e

    return res_sort_by_likes, res_sort_by_date


def get_top_noteworthy_posts(filter: Filter, db_collection: str):
    """
    Query the db based on user filter to get top noteworthy related comments based on likes

    Args:
        filter (Filter): JSON request body (user's filter options)

    Raises:
        HTTPException: For data type error, using pydantic

    Returns:
        list: List of records(sorted by likes and dates)
    """
    project = {
        "topic": 1,
        "sentiment": "$sentiment_label",
        "emotion": "$emotions_label",
        "intent": 1,
        "_id": False,
    }

    if "facebook" in db_collection:
        db_query = db_filter_query_from_user_filter(filter, datetime_str=FB_DATETIME_STR)
        likes_key = "likes_cnt"
        datetime_key = "created_time"
        project["comment"] = "$message"
    elif "twitter" in db_collection:
        db_query = db_filter_query_from_user_filter(filter, datetime_str=TWIT_DATETIME_STR)
        likes_key = "likes_count"
        datetime_key = "created_at"
        project["comment"] = "$tweet"
    elif "reddit" in db_collection:
        db_query = db_filter_query_from_user_filter(filter, datetime_str=REDDIT_DATETIME_STR)
        likes_key = "score"
        datetime_key = REDDIT_DATETIME_STR
        project["comment"] = "$title"
    elif "youtube" in db_collection:
        db_query = db_filter_query_from_user_filter(filter, datetime_str=REDDIT_DATETIME_STR)
        likes_key = "likes"
        datetime_key = YT_DATETIME_STR
        project["comment"] = "$combined_text"
    project["likes"] = f"${likes_key}"
    project["datetime"] = f"${datetime_key}"

    db_query["isNoteworthy"] = 1

    res_sort_by_likes = list(db[db_collection].find(db_query, project).sort(likes_key, -1).limit(filter.topN))
    res_sort_by_date = list(
        db[db_collection].find(db_query, project).sort(datetime_key, -1).limit(filter.topN)
    )

    try:
        Top5ComplaintOrNoteworthyPostsRes(data=res_sort_by_likes)
        Top5ComplaintOrNoteworthyPostsRes(data=res_sort_by_date)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e

    return res_sort_by_likes, res_sort_by_date


def get_top5_noteworthy_topics(filter: Filter, project: dict, db_collection: str):
    """
    Query the db based on user filter to get top 5 topics for noteworthy related mentions based on likes

    Args:
        filter (Filter): JSON request body (user's filter options)
        project (dict): MongoDB project field for query statement
        db_collection (str): To determine which collection to query from

    Raises:
        HTTPException: For data type error, using pydantic

    Returns:
        list: List of records
    """
    if "facebook" in db_collection:
        db_query = db_filter_query_from_user_filter(filter, datetime_str=FB_DATETIME_STR)
    elif "twitter" in db_collection:
        db_query = db_filter_query_from_user_filter(filter, datetime_str=TWIT_DATETIME_STR)
    elif "reddit" in db_collection:
        db_query = db_filter_query_from_user_filter(filter, datetime_str=REDDIT_DATETIME_STR)
    elif "youtube" in db_collection:
        db_query = db_filter_query_from_user_filter(filter, datetime_str=YT_DATETIME_STR)
    db_query["isNoteworthy"] = 1

    res = list(db[db_collection].find(db_query, project))

    try:
        Top5NoteworthyTopicsRes(data=res)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e

    return res


def get_complaint_mentions_count(filter: Filter, db_collection: str):
    """
    Query db based on user filter to get number of complaint mentions count

    Args:
        filter (Filter): JSON request body (user's filter options)
        db_collection (str): To determine which collection to query from

    Returns:
        int: Number of complaint mentions count
    """
    if "facebook" in db_collection:
        db_query = db_filter_query_from_user_filter(filter, datetime_str=FB_DATETIME_STR)
    elif "twitter" in db_collection:
        db_query = db_filter_query_from_user_filter(filter, datetime_str=TWIT_DATETIME_STR)
    elif "reddit" in db_collection:
        db_query = db_filter_query_from_user_filter(filter, datetime_str=REDDIT_DATETIME_STR)
    elif "youtube" in db_collection:
        db_query = db_filter_query_from_user_filter(filter, datetime_str=YT_DATETIME_STR)
    db_query["intent"] = {"$regex": "complaint"}

    return len(list(db[db_collection].find(db_query)))


def get_mentions_count(filter: Filter, db_collection: str):
    """
    Query db based on user filter to get number of mentions count

    Args:
        filter (Filter): JSON request body (user's filter options)
        db_collection (str): To determine which collection to query from

    Returns:
        int: Number of mentions count
    """
    if "facebook" in db_collection:
        db_query = db_filter_query_from_user_filter(filter, datetime_str=FB_DATETIME_STR)
    elif "twitter" in db_collection:
        db_query = db_filter_query_from_user_filter(filter, datetime_str=TWIT_DATETIME_STR)
    elif "reddit" in db_collection:
        db_query = db_filter_query_from_user_filter(filter, datetime_str=REDDIT_DATETIME_STR)
    elif "youtube" in db_collection:
        db_query = db_filter_query_from_user_filter(filter, datetime_str=YT_DATETIME_STR)

    return len(list(db[db_collection].find(db_query)))
