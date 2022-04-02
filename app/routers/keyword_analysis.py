from collections import Counter
from typing import List

import pandas as pd
from fastapi import APIRouter

from ..schema.keyword_analysis import Top20KeywordAnalysisRes
from ..schema.user_filter import Filter
from .facebook import get_top_keywords

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

    filter1 = Filter(
        endDate="2019-03-01",
        numDays=14,
        platforms=["Facebook", "Reddit"],
        sentiments=["positive", "negative", "neutral"],
        emotions=["joy", "sadness", "neutral", "anger", "fear"],
        query=None,
    )

    data1 = get_top_keywords(filter, project)
    data2 = get_top_keywords(filter1, project)

    all_data = data1 + data2

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

    entities = df["entities"].to_list()
    entities_count = Counter(entities).most_common()

    res = []
    for i, ent in enumerate(entities_count):
        if i >= 20:
            break

        res.append(
            {
                "word": ent[0],
                "count": ent[1],
                "sentiment": ent_sentiment[ent_sentiment["entities"] == ent[0]][
                    "sentiment_label"
                ].values[0],
            }
        )
    return res
