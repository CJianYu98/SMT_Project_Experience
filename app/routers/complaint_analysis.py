from collections import Counter
from typing import List

import pandas as pd
from fastapi import APIRouter

from ..dao.facebook import get_top5_complaint_comments, get_top_complaint_keywords
from ..schema.complaint_analysis import Top20ComplaintKeywordAnalysisRes
from ..schema.user_filter import Filter

router = APIRouter(prefix="/complaint-analysis", tags=["complaint_analysis"])


@router.post(
    "/get-all-top-complaint-keywords", response_model=List[Top20ComplaintKeywordAnalysisRes]
)
def get_all_top_complaint_keywords(filter: Filter):
    """
    To get top 20 keywords (based on counts) for complaint related records

    Args:
        filter (Filter): JSON request body (user's filter options)

    Returns:
        Pydantic Model: JSON response object
    """
    project = {"entities": 1, "_id": False}

    # Query selected social media platform MongoDB collection based on user platform filter options
    if "facebook" in filter.platforms:
        fb_posts_data = get_top_complaint_keywords(filter, project, "posts")
        fb_comments_data = get_top_complaint_keywords(filter, project, "comments")
    else:
        fb_posts_data = fb_comments_data = []

    # Concat data from all social media platforms
    all_data = sum([fb_posts_data, fb_comments_data], [])

    # Remove records with no entities using pandas
    df = pd.DataFrame(all_data)
    df = df.explode("entities")
    df.dropna(inplace=True)

    # Get the counts for each entity, in descending ordering
    entities = df["entities"].to_list()
    entities_count = Counter(entities).most_common()

    res = []
    if len(entities_count) >= 20:
        res.extend(
            {
                "word": entities_count[i][0],
                "count": entities_count[i][1],
            }
            for i in range(20)
        )
    else:
        res.extend(
            {
                "word": entities_count[i][0],
                "count": entities_count[i][1],
            }
            for i in range(len(entities_count))
        )
    return res


@router.post("/get-all-top5-complaint-comments")
def get_all_top5_complaint_comments(filter: Filter):

    # Query selected social media platform MongoDB collection based on user platform filter options
    if "facebook" in filter.platforms:
        fb_comments_by_likes, fb_comments_by_date = get_top5_complaint_comments(filter)
    else:
        fb_comments_by_likes = fb_comments_by_date = []

    return {"facebook": {"likes": fb_comments_by_likes, "date": fb_comments_by_date}}
