from collections import Counter
from typing import List

import pandas as pd
from fastapi import APIRouter

from ..schema.complaint_analysis import Top20ComplaintKeywordAnalysisRes
from ..schema.user_filter import Filter
from .facebook import get_top_complaint_keywords

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

    filter1 = Filter(
        endDate="2019-03-01",
        numDays=14,
        platforms=["facebook", "reddit"],
        sentiments=["positive", "negative", "neutral"],
        emotions=["joy", "sadness", "neutral", "anger", "fear"],
        query=None,
    )

    data1 = get_top_complaint_keywords(filter, project)
    data2 = get_top_complaint_keywords(filter1, project)

    all_data = data1 + data2

    df = pd.DataFrame(all_data)
    df = df.explode("entities")
    df.dropna(inplace=True)

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
