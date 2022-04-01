from collections import Counter

import pandas as pd
from typing import List
from fastapi import APIRouter, HTTPException

from ..schema.topic_analysis import IndiTopicStatsRes
from ..schema.user_filter import Filter
from .facebook import get_fb_top5_topics_stats

router = APIRouter(prefix="/topic-analysis", tags=["topic_analysis"])


@router.post("/get-top5-topic-analysis", response_model=List[IndiTopicStatsRes])
async def get_top5_topic_analysis(filter: Filter):
    """
    Generate top 5 topics and their respective statistics (sentiments, emotions, top mentions, counts)

    Args:
        filter (Filter): JSON request body, containing user filter options, for querying db

    Returns:
        Pydantic Model: JSON response object
    """

    # Create MongoDB project field in query statement
    project = {
        "entities": 1,
        "emotions_label": 1,
        "sentiment_label": 1,
        "topic": 1,
        "message": 1,
        "_id": False,
    }

    filter1 = Filter(
        start_date="2021-02-01",
        end_date="2021-03-01",
        platforms=["Facebook", "Reddit"],
        sentiments=["positive", "negative", "neutral"],
        emotions=["joy", "sadness", "neutral", "anger", "fear"],
        query=None,
    )

    fb_data = get_fb_top5_topics_stats(filter, project)
    fb_data1 = get_fb_top5_topics_stats(filter1, project)

    # May need to rename the column names for each df, and concat to empty df instead
    all_data = fb_data + fb_data1
    if not all_data:
        raise HTTPException(
            status_code=404,
            detail=f"No data found within date period {filter.start_date} to {filter.end_date}",
        )
    df = pd.DataFrame(all_data)

    # Getting the top 5 topics
    topics_groupby = (
        df.groupby("topic").size().sort_values(ascending=False).to_frame("size").reset_index()
    )
    top_5_topics = [topics_groupby.iloc[i]["topic"] for i in range(len(topics_groupby)) if i < 5]

    # Create top sentiment and emotions df for each topic, using groupby (by topic, sentiment/emotions)
    top_5_topics_filtered = df[df["topic"].isin(top_5_topics)]
    top_sentiment_per_topic = (
        top_5_topics_filtered.groupby(["topic", "sentiment_label"])
        .size()
        .sort_values(ascending=False)
        .to_frame("size")
        .reset_index()
    )
    top_emotions_per_topic = (
        top_5_topics_filtered.groupby(["topic", "emotions_label"])
        .size()
        .sort_values(ascending=False)
        .to_frame("size")
        .reset_index()
    )

    # Create response object
    res = []

    # Generate stats for each topic
    for topic in top_5_topics:
        # Filter df with records pertaining to the topic
        topic_sentiment_stats_df = top_sentiment_per_topic[
            top_sentiment_per_topic["topic"] == topic
        ]
        topic_emotions_stats_df = top_emotions_per_topic[top_emotions_per_topic["topic"] == topic]

        # Calc number of mentions for each topic
        mentions = len(df[df["topic"] == topic])

        # Retrieve sentiment stats for each topic
        topic_sentiment_stats = [
            {
                "sentiment": topic_sentiment_stats_df.iloc[i]["sentiment_label"],
                "count": int(topic_sentiment_stats_df.iloc[i]["size"]),
            }
            for i in range(len(topic_sentiment_stats_df))
        ]

        # Retrieve emotion stats for each topic
        topic_emotions_stats = [
            {
                "emotion": topic_emotions_stats_df.iloc[j]["emotions_label"],
                "count": int(topic_emotions_stats_df.iloc[j]["size"]),
            }
            for j in range(len(topic_emotions_stats_df))
        ]

        # Retrieve top 3 mentions for each topic
        topic_df = top_5_topics_filtered[top_5_topics_filtered["topic"] == topic]
        topic_entities = topic_df["entities"].sum()
        topic_entities_count = Counter(topic_entities).most_common()
        if len(topic_entities_count) >= 3:
            top3_mentions = [topic_entities_count[k][0] for k in range(3)]
        else:
            top3_mentions = [topic_entities_count[k][0] for k in range(len(topic_entities_count))]

        # Add topic stats to response object
        res.append(
            {
                "name": topic,
                "mentions": mentions,
                "topThreeMentions": top3_mentions,
                "sentiment": topic_sentiment_stats,
                "emotions": topic_emotions_stats,
            }
        )

    assert len(res) == 5

    return res
