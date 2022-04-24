import os

from fastapi import APIRouter

from ..dao.dao import get_top_posts
from ..schema.top_posts import TopPostsSortedRes
from ..schema.user_filter import Filter

router = APIRouter(prefix="/top-posts", tags=["top_posts"])

# Declare MongoDB collection names to interact with
FB_POSTS = os.getenv("DB_FACEBOOK_POSTS_COLLECTION")
FB_COMMENTS = os.getenv("DB_FACEBOOK_COMMENTS_COLLECTION")
TWITTER_TWEETS = os.getenv("DB_TWIITER_TWEETS_COLLECTION")
TWITTER_COMMENTS = os.getenv("DB_TWITTER_COMMENTS_COLLECTION")
REDDIT_SUBMISSIONS = os.getenv("DB_REDDIT_SUBMISSIONS_COLLECTION")
REDDIT_COMMENTS = os.getenv("DB_REDDIT_COMMENTS_COLLECTION")
YOUTUBE_VIDEOS = os.getenv("DB_YOUTUBE_VIDEOS_COLLECTION")
YOUTUBE_COMMENTS = os.getenv("DB_YOUTUBE_COMMENTS_COLLECTION")


@router.post(
    "/get-all-top-posts",
    response_model=TopPostsSortedRes,
    response_model_exclude_none=True,
)
def get_all_top_posts(filter: Filter):
    """
    To get top 5 likes comments for complaint related comments

    Args:
        filter (Filter): JSON request body (user's filter options)

    Returns:
        Pydantic Model: JSON response object
    """

    # Create response body
    res = {}

    # Query selected social media platform MongoDB collection based on user platform filter options
    if "facebook" in filter.platforms:
        fb_comments_by_likes, fb_comments_by_date = get_top_posts(filter, FB_POSTS)
        res["facebook"] = {"likes": fb_comments_by_likes, "date": fb_comments_by_date}
    if "twitter" in filter.platforms:
        twit_comments_by_likes, twit_comments_by_date = get_top_posts(filter, TWITTER_TWEETS)
        res["twitter"] = {"likes": twit_comments_by_likes, "date": twit_comments_by_date}
    if "reddit" in filter.platforms:
        reddit_comments_by_likes, reddit_comments_by_date = get_top_posts(
            filter, REDDIT_SUBMISSIONS
        )
        res["reddit"] = {"likes": reddit_comments_by_likes, "date": reddit_comments_by_date}
    if "youtube" in filter.platforms:
        youtube_comments_by_likes, youtube_comments_by_date = get_top_posts(filter, YOUTUBE_VIDEOS)
        res["youtube"] = {"likes": youtube_comments_by_likes, "date": youtube_comments_by_date}

    return res
