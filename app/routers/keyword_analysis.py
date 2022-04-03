from collections import Counter
from typing import List

import pandas as pd
from fastapi import APIRouter

from ..schema.keyword_analysis import Top20KeywordAnalysisRes
from ..schema.user_filter import Filter
from ..dao.facebook import get_top_keywords

router = APIRouter(prefix="/keyword-analysis", tags=["keyword_analysis"])


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
        fb_posts_data = get_top_keywords(filter, project, "posts")
        fb_comments_data = get_top_keywords(filter, project, "comments")
    else:
        fb_posts_data = fb_comments_data = []

    # Concat data from all social media platforms
    all_data = sum([fb_posts_data, fb_comments_data], [])

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
    if len(entities_count) >= 20:
        res.extend(
            {
                "word": entities_count[i][0],
                "count": entities_count[i][1],
                "sentiment": ent_sentiment[ent_sentiment["entities"] == entities_count[i][0]][
                    "sentiment_label"
                ].values[0],
            }
            for i in range(20)
        )
    else:
        res.extend(
            {
                "word": entities_count[i][0],
                "count": entities_count[i][1],
                "sentiment": ent_sentiment[ent_sentiment["entities"] == entities_count[i][0]][
                    "sentiment_label"
                ].values[0],
            }
            for i in range(len(entities_count))
        )

    return res
