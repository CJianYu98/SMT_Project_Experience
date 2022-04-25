from datetime import datetime, timedelta

from ..schema.user_filter import Filter


def db_filter_query_from_user_filter(filter: Filter, datetime_str: str, db_collection: str) -> dict:
    end_date = datetime.strptime(filter.endDate, "%Y-%m-%d")
    start_date = end_date - timedelta(days=filter.numDays)

    db_query = {
        datetime_str: {"$gte": start_date, "$lte": end_date},
        "sentiment_label": {"$in": filter.sentiments},
        "emotions_label": {"$in": filter.emotions},
    }

    if filter.query:
        if "facebook" in db_collection:
            db_query["message"] = {"$regex": f" {filter.query} "}
        elif "twitter" in db_collection:
            db_query["tweet"] = {"$regex": f" {filter.query} "}
        elif db_collection in {"reddit_submissions", "youtube_videos"}:
            db_query["combined_text"] = {"$regex": f" {filter.query} "}
        elif db_collection == "reddit_comments":
            db_query["body"] = {"$regex": f" {filter.query} "}
        elif db_collection == "youtube_comments":
            db_query["comment"] = {"$regex": f" {filter.query} "}

    return db_query
