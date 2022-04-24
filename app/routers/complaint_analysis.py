import os
from collections import Counter
from typing import List

import pandas as pd
from fastapi import APIRouter, HTTPException

from ..dao.dao import (
    get_complaint_mentions_count,
    get_mentions_count,
    get_top5_complaint_posts,
    get_top_complaint_keywords,
)
from ..schema.complaint_analysis import (
    ComplaintPercentageRes,
    Top5ComplaintPostsRes,
    Top20ComplaintKeywordAnalysisRes,
)
from ..schema.user_filter import Filter

router = APIRouter(prefix="/complaint-analysis", tags=["complaint_analysis"])

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
    if "reddit" in filter.platforms:
        reddit_submissions_data = get_top_complaint_keywords(filter, project, REDDIT_SUBMISSIONS)
        reddit_comments_data = get_top_complaint_keywords(filter, project, REDDIT_COMMENTS)
    else:
        reddit_submissions_data = reddit_comments_data = []
    if "youtube" in filter.platforms:
        youtube_vidoes_data = get_top_complaint_keywords(filter, project, YOUTUBE_VIDEOS)
        youtube_comments_data = get_top_complaint_keywords(filter, project, YOUTUBE_COMMENTS)
    else:
        youtube_vidoes_data = youtube_comments_data = []

    # Concat data from all social media platforms
    all_data = sum(
        [
            fb_posts_data,
            fb_comments_data,
            twit_tweets_data,
            twit_comments_data,
            reddit_submissions_data,
            reddit_comments_data,
            youtube_vidoes_data,
            youtube_comments_data,
        ],
        [],
    )
    if not all_data:
        raise HTTPException(status_code=404, detail="No data found within date period given")

    # Remove records with no entities using pandas
    df = pd.DataFrame(all_data)
    df = df.explode("entities")
    df.dropna(inplace=True)

    # Get the counts for each entity, in descending ordering
    entities = df["entities"].to_list()
    entities_count = Counter(entities).most_common()

    res = []
    for i in range(len(entities_count)):
        if i >= filter.topN:
            break

        res.append(
            {
                "word": entities_count[i][0],
                "count": entities_count[i][1],
            }
        )

    return res


@router.post(
    "/get-all-top5-complaint-posts",
    response_model=Top5ComplaintPostsRes,
    response_model_exclude_none=True,
)
def get_all_top5_complaint_posts(filter: Filter):
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
        fb_comments_by_likes, fb_comments_by_date = get_top5_complaint_posts(filter, FB_POSTS)
        res["facebook"] = {"likes": fb_comments_by_likes, "date": fb_comments_by_date}
    if "twitter" in filter.platforms:
        twit_comments_by_likes, twit_comments_by_date = get_top5_complaint_posts(
            filter, TWITTER_TWEETS
        )
        res["twitter"] = {"likes": twit_comments_by_likes, "date": twit_comments_by_date}
    if "reddit" in filter.platforms:
        reddit_comments_by_likes, reddit_comments_by_date = get_top5_complaint_posts(
            filter, REDDIT_SUBMISSIONS
        )
        res["reddit"] = {"likes": reddit_comments_by_likes, "date": reddit_comments_by_date}
    if "youtube" in filter.platforms:
        youtube_comments_by_likes, youtube_comments_by_date = get_top5_complaint_posts(
            filter, YOUTUBE_VIDEOS
        )
        res["youtube"] = {"likes": youtube_comments_by_likes, "date": youtube_comments_by_date}

    return res


@router.post(
    "/get-platform-complaint-percentage",
    response_model=ComplaintPercentageRes,
    response_model_exclude_none=True,
)
def get_platform_complaint_percentage(filter: Filter):
    """
    To get percentage of complaint mentions for each platform

    Args:
        filter (Filter): JSON request body (user's filter options)

    Returns:
        Pydantic Model: JSON response object
    """

    # Create response body
    res = {}

    # Query selected social media platform MongoDB collection based on user platform filter options
    if "facebook" in filter.platforms:
        fb_posts_complaint_count = get_complaint_mentions_count(filter, FB_POSTS)
        fb_comments_complaint_count = get_complaint_mentions_count(filter, FB_COMMENTS)
        fb_posts_mention_count = get_mentions_count(filter, FB_POSTS)
        fb_comments_mention_count = get_mentions_count(filter, FB_COMMENTS)

        if (fb_posts_mention_count + fb_comments_mention_count) == 0:
            facebook_complaint_perc = 0
        else:
            facebook_complaint_perc = round(
                (fb_posts_complaint_count + fb_comments_complaint_count)
                / (fb_posts_mention_count + fb_comments_mention_count),
                2,
            )
        res["facebook"] = facebook_complaint_perc
    if "twitter" in filter.platforms:
        twitter_tweets_complaint_count = get_complaint_mentions_count(filter, TWITTER_TWEETS)
        twitter_comments_complaint_count = get_complaint_mentions_count(filter, TWITTER_COMMENTS)
        twitter_tweets_mention_count = get_mentions_count(filter, TWITTER_TWEETS)
        twitter_comments_mention_count = get_mentions_count(filter, TWITTER_COMMENTS)

        if (twitter_tweets_mention_count + twitter_comments_mention_count) == 0:
            twitter_complaint_perc = 0
        else:
            twitter_complaint_perc = round(
                (twitter_tweets_complaint_count + twitter_comments_complaint_count)
                / (twitter_tweets_mention_count + twitter_comments_mention_count),
                2,
            )
        res["twitter"] = twitter_complaint_perc
    if "reddit" in filter.platforms:
        reddit_submissions_complaint_count = get_complaint_mentions_count(
            filter, REDDIT_SUBMISSIONS
        )
        reddit_comments_complaint_count = get_complaint_mentions_count(filter, REDDIT_COMMENTS)
        reddit_submissions_mention_count = get_mentions_count(filter, REDDIT_SUBMISSIONS)
        reddit_comments_mention_count = get_mentions_count(filter, REDDIT_COMMENTS)

        if (reddit_submissions_mention_count + reddit_comments_mention_count) == 0:
            reddit_complaint_perc = 0
        else:
            reddit_complaint_perc = round(
                (reddit_submissions_complaint_count + reddit_comments_complaint_count)
                / (reddit_submissions_mention_count + reddit_comments_mention_count),
                2,
            )
        res["reddit"] = reddit_complaint_perc
    if "youtube" in filter.platforms:
        youtube_videos_complaint_count = get_complaint_mentions_count(filter, YOUTUBE_VIDEOS)
        youtube_comments_complaint_count = get_complaint_mentions_count(filter, YOUTUBE_COMMENTS)
        youtube_videos_mention_count = get_mentions_count(filter, YOUTUBE_VIDEOS)
        youtube_comments_mention_count = get_mentions_count(filter, YOUTUBE_COMMENTS)

        if (youtube_videos_mention_count + youtube_comments_mention_count) == 0:
            youtube_complaint_perc = 0
        else:
            youtube_complaint_perc = round(
                (youtube_videos_complaint_count + youtube_comments_complaint_count)
                / (youtube_videos_mention_count + youtube_comments_mention_count),
                2,
            )
        res["youtube"] = youtube_complaint_perc

    return res
