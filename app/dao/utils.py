from ..database.connect import db


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
