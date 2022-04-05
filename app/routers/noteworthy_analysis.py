import os
from collections import Counter

from fastapi import APIRouter

from ..dao.dao import get_top5_noteworthy_comments
from ..schema.complaint_noteworthy_analysis import Top5ComplaintOrNoteworthyCommentsRes
from ..schema.user_filter import Filter

router = APIRouter(prefix="/noteworthy-analysis", tags=["noteworthy_analysis"])

# Declare MongoDB collection names to interact with
# FB_POSTS = os.getenv("DB_FACEBOOK_POSTS_COLLECTION")
# FB_COMMENTS = os.getenv("DB_FACEBOOK_COMMENTS_COLLECTION")
FB_POSTS = "facebook_posts_v1"
FB_COMMENTS = "facebook_comments_v1"
TWITTER_TWEETS = os.getenv("DB_TWIITER_TWEETS_COLLECTION")
TWITTER_COMMENTS = os.getenv("DB_TWITTER_COMMENTS_COLLECTION")


@router.post(
    "/get-all-top5-noteworthy-comments", response_model=Top5ComplaintOrNoteworthyCommentsRes
)
def get_all_top5_noteworthy_comments(filter: Filter):
    """
    To get top 5 likes comments for noteworthy related comments

    Args:
        filter (Filter): _description_

    Returns:
        Pydantic Model: JSON response object
    """

    # Query selected social media platform MongoDB collection based on user platform filter options
    if "facebook" in filter.platforms:
        fb_comments_by_likes, fb_comments_by_date = get_top5_noteworthy_comments(filter, FB_POSTS)
    else:
        fb_comments_by_likes = fb_comments_by_date = []
    if "twitter" in filter.platforms:
        twit_comments_by_likes, twit_comments_by_date = get_top5_noteworthy_comments(
            filter, TWITTER_TWEETS
        )
    else:
        twit_comments_by_likes = twit_comments_by_date = []

    return {
        "facebook": {"likes": fb_comments_by_likes, "date": fb_comments_by_date},
        "twitter": {"likes": twit_comments_by_likes, "date": twit_comments_by_date},
    }