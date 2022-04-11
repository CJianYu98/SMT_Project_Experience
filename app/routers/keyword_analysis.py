import os
from collections import Counter
from typing import List

import pandas as pd
from fastapi import APIRouter, HTTPException

from ..dao.dao import get_top_keywords
from ..schema.keyword_analysis import Top20KeywordAnalysisRes
from ..schema.user_filter import Filter

router = APIRouter(prefix="/keyword-analysis", tags=["keyword_analysis"])

# Declare MongoDB collection names to interact with
# FB_POSTS = os.getenv("DB_FACEBOOK_POSTS_COLLECTION")
# FB_COMMENTS = os.getenv("DB_FACEBOOK_COMMENTS_COLLECTION")
FB_POSTS = "facebook_posts_v1"
FB_COMMENTS = "facebook_comments_v1"
TWITTER_TWEETS = os.getenv("DB_TWIITER_TWEETS_COLLECTION")
TWITTER_COMMENTS = os.getenv("DB_TWITTER_COMMENTS_COLLECTION")
REDDIT_SUBMISSIONS = os.getenv("DB_REDDIT_SUBMISSIONS_COLLECTION")
REDDIT_COMMENTS = os.getenv("DB_REDDIT_COMMENTS_COLLECTION")
YOUTUBE_VIDEOS = os.getenv("DB_YOUTUBE_VIDEOS_COLLECTION")
YOUTUBE_COMMENTS = os.getenv("DB_YOUTUBE_COMMENTS_COLLECTION")


@router.post("/get-all-top-keywords", response_model=List[Top20KeywordAnalysisRes])
def get_all_top_keywords(filter: Filter):
    """
    To get top 20 keywords (based on counts)

    Args:
        filter (Filter): JSON request body (user's filter options)

    Returns:
        Pydantic Model: JSON response object
    """
    project = {"sentiment_label": 1, "entities": 1, "_id": False}

    # Query selected social media platform MongoDB collection based on user platform filter options
    if "facebook" in filter.platforms:
        fb_posts_data = get_top_keywords(filter, project, FB_POSTS)
        fb_comments_data = get_top_keywords(filter, project, FB_COMMENTS)
    else:
        fb_posts_data = fb_comments_data = []
    if "twitter" in filter.platforms:
        twit_tweets_data = get_top_keywords(filter, project, TWITTER_TWEETS)
        twit_comments_data = get_top_keywords(filter, project, TWITTER_COMMENTS)
    else:
        twit_tweets_data = twit_comments_data = []
    if "reddit" in filter.platforms:
        reddit_submissions_data = get_top_keywords(filter, project, REDDIT_SUBMISSIONS)
        reddit_comments_data = get_top_keywords(filter, project, REDDIT_COMMENTS)
    else:
        reddit_submissions_data = reddit_comments_data = []
    if "youtube" in filter.platforms:
        youtube_videos_data = get_top_keywords(filter, project, YOUTUBE_VIDEOS)
        youtube_comments_data = get_top_keywords(filter, project, YOUTUBE_COMMENTS)
    else:
        youtube_videos_data = youtube_comments_data = []

    # Concat data from all social media platforms
    all_data = sum(
        [
            fb_posts_data,
            fb_comments_data,
            twit_tweets_data,
            twit_comments_data,
            reddit_submissions_data,
            reddit_comments_data,
            youtube_videos_data,
            youtube_comments_data
        ],
        [],
    )
    if not all_data:
        raise HTTPException(status_code=404, detail="No data found within date period given")

    # Using pandas to group by entities and sentiment_label and get the counts
    df = pd.DataFrame(all_data)
    df = df.explode("entities")
    df.dropna(inplace=True)
    df.reset_index(drop=True, inplace=True)
    ent_sentiment = (
        df.groupby(["entities", "sentiment_label"])
        .size()
        .sort_values(ascending=False)
        .to_frame("size")
        .reset_index()
    )

    # Get the counts for each entity, in descending ordering
    entities = df["entities"].to_list()
    entities_count = Counter(entities).most_common()

    res = []
    for i in range(len(entities_count)):
        if i >= 20:
            break

        res.append(
            {
                "word": entities_count[i][0],
                "count": entities_count[i][1],
                "sentiment": ent_sentiment[ent_sentiment["entities"] == entities_count[i][0]][
                    "sentiment_label"
                ].values[0],
            }
        )

    return res
