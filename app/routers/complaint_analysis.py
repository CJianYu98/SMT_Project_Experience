import os
from collections import Counter
from typing import List

import pandas as pd
from fastapi import APIRouter

from ..dao.dao import get_top5_complaint_comments, get_top_complaint_keywords
from ..schema.complaint_noteworthy_analysis import (
    Top5ComplaintOrNoteworthyCommentsRes,
    Top20ComplaintKeywordAnalysisRes,
)
from ..schema.user_filter import Filter

router = APIRouter(prefix="/complaint-analysis", tags=["complaint_analysis"])

# Declare MongoDB collection names to interact with
# FB_POSTS = os.getenv("DB_FACEBOOK_POSTS_COLLECTION")
# FB_COMMENTS = os.getenv("DB_FACEBOOK_COMMENTS_COLLECTION")
FB_POSTS = "facebook_posts_v1"
FB_COMMENTS = "facebook_comments_v1"
TWITTER_TWEETS = os.getenv("DB_TWIITER_TWEETS_COLLECTION")
TWITTER_COMMENTS = os.getenv("DB_TWITTER_COMMENTS_COLLECTION")


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
        fb_posts_data = get_top_complaint_keywords(filter, project, FB_POSTS)
        fb_comments_data = get_top_complaint_keywords(filter, project, FB_COMMENTS)
    else:
        fb_posts_data = fb_comments_data = []
    if "twitter" in filter.platforms:
        twit_tweets_data = get_top_complaint_keywords(filter, project, TWITTER_TWEETS)
        twit_comments_data = get_top_complaint_keywords(filter, project, TWITTER_COMMENTS)
    else:
        twit_tweets_data = twit_comments_data = []

    # Concat data from all social media platforms
    all_data = sum([fb_posts_data, fb_comments_data, twit_tweets_data, twit_comments_data], [])

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


@router.post(
    "/get-all-top5-complaint-comments", response_model=Top5ComplaintOrNoteworthyCommentsRes
)
def get_all_top5_complaint_comments(filter: Filter):
    """
    To get top 5 likes comments for complaint related comments

    Args:
        filter (Filter): JSON request body (user's filter options)

    Returns:
        Pydantic Model: JSON response object
    """

    # Query selected social media platform MongoDB collection based on user platform filter options
    if "facebook" in filter.platforms:
        fb_comments_by_likes, fb_comments_by_date = get_top5_complaint_comments(filter, FB_POSTS)
    else:
        fb_comments_by_likes = fb_comments_by_date = []
    if "twitter" in filter.platforms:
        twit_comments_by_likes, twit_comments_by_date = get_top5_complaint_comments(
            filter, TWITTER_TWEETS
        )
    else:
        twit_comments_by_likes = twit_comments_by_date = []

    return {
        "facebook": {"likes": fb_comments_by_likes, "date": fb_comments_by_date},
        "twitter": {"likes": twit_comments_by_likes, "date": twit_comments_by_date},
    }