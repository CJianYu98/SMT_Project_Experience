import os
from collections import Counter
from typing import List

from fastapi import APIRouter

from ..dao.dao import get_top_noteworthy_posts, get_top5_noteworthy_topics
from ..schema.noteworthy_analysis import Top5NoteworthyPostsRes
from ..schema.user_filter import Filter

router = APIRouter(prefix="/noteworthy-analysis", tags=["noteworthy_analysis"])

# Declare MongoDB collection names to interact with
FB_POSTS = os.getenv("DB_FACEBOOK_POSTS_COLLECTION")
FB_COMMENTS = os.getenv("DB_FACEBOOK_COMMENTS_COLLECTION")
TWITTER_TWEETS = os.getenv("DB_TWIITER_TWEETS_COLLECTION")
TWITTER_COMMENTS = os.getenv("DB_TWITTER_COMMENTS_COLLECTION")
REDDIT_SUBMISSIONS = os.getenv("DB_REDDIT_SUBMISSIONS_COLLECTION")
REDDIT_COMMENTS = os.getenv("DB_REDDIT_COMMENTS_COLLECTION")
YOUTUBE_VIDEOS = os.getenv("DB_YOUTUBE_VIDEOS_COLLECTION")
YOUTUBE_COMMENTS = os.getenv("DB_YOUTUBE_COMMENTS_COLLECTION")


@router.post("/get-all-top5-noteworthy-posts", response_model=Top5NoteworthyPostsRes)
def get_all_top5_noteworthy_posts(filter: Filter):
    """
    To get top 5 likes comments for noteworthy related comments

    Args:
        filter (Filter): _description_

    Returns:
        Pydantic Model: JSON response object
    """

    # Query selected social media platform MongoDB collection based on user platform filter options
    if "facebook" in filter.platforms:
        fb_comments_by_likes, fb_comments_by_date = get_top_noteworthy_posts(filter, FB_POSTS)
    else:
        fb_comments_by_likes = fb_comments_by_date = []
    if "twitter" in filter.platforms:
        twit_comments_by_likes, twit_comments_by_date = get_top_noteworthy_posts(
            filter, TWITTER_TWEETS
        )
    else:
        twit_comments_by_likes = twit_comments_by_date = []
    if "reddit" in filter.platforms:
        reddit_comments_by_likes, reddit_comments_by_date = get_top_noteworthy_posts(
            filter, REDDIT_SUBMISSIONS
        )
    else:
        reddit_comments_by_likes = reddit_comments_by_date = []
    if "youtube" in filter.platforms:
        youtube_comments_by_likes, youtube_comments_by_date = get_top_noteworthy_posts(
            filter, YOUTUBE_VIDEOS
        )
    else:
        youtube_comments_by_likes = youtube_comments_by_date = []

    return {
        "facebook": {"likes": fb_comments_by_likes, "date": fb_comments_by_date},
        "twitter": {"likes": twit_comments_by_likes, "date": twit_comments_by_date},
        "reddit": {"likes": reddit_comments_by_likes, "date": reddit_comments_by_date},
        "youtube": {"likes": youtube_comments_by_likes, "date": youtube_comments_by_date}
    }


@router.post("/get-all-top5-noteworthy-topics", response_model=List[str])
def get_all_top5_noteworthy_topics(filter: Filter):
    """
    To get top 5 topics for noteworthy mentions (based on counts)

    Args:
        filter (Filter): JSON request body (user's filter options)

    Returns:
        Pydantic Model: JSON response object
    """
    project = {"_id": False, "topic": 1}

    # Query selected social media platform MongoDB collection based on user platform filter options
    if "facebook" in filter.platforms:
        fb_posts_data = get_top5_noteworthy_topics(filter, project, FB_POSTS)
    else:
        fb_posts_data = []
    if "twitter" in filter.platforms:
        twit_tweets_data = get_top5_noteworthy_topics(filter, project, TWITTER_TWEETS)
    else:
        twit_tweets_data = []
    if "reddit" in filter.platforms:
        reddit_submissions_data = get_top5_noteworthy_topics(filter, project, REDDIT_SUBMISSIONS)
    else:
        reddit_submissions_data = []
    if "youtube" in filter.platforms:
        youtube_videos_data = get_top5_noteworthy_topics(filter, project, YOUTUBE_VIDEOS)
    else:
        youtube_videos_data = []

    # Concat data from all social media platforms
    all_data = sum(
        [
            fb_posts_data,
            twit_tweets_data,
            reddit_submissions_data,
            youtube_videos_data
        ],
        [],
    )

    # Get counts for each topic, in descending order
    all_topics = [data["topic"] for data in all_data]
    topics_count = Counter(all_topics).most_common()

    res = []
    for i in range(len(topics_count)):
        if i >= filter.topN:
            break

        res.append(topics_count[i][0])

    return res
