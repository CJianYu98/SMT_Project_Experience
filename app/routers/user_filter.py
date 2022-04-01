from datetime import datetime, timedelta

from ..schema.user_filter import Filter


def db_filter_query_from_user_filter(filter: Filter) -> dict:
    endDate = datetime.strptime(filter.endDate, "%Y-%m-%d")
    start_date = endDate - timedelta(days=filter.numDays)

    db_query = {
        "created_time": {"$gte": start_date, "$lte": endDate},
        "sentiment_label": {"$in": filter.sentiments},
        "emotions_label": {"$in": filter.emotions},
    }
    if filter.query:
        db_query["message"] = {"$regex": f" {filter.query} "}

    return db_query
