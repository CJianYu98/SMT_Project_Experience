from typing import List

from pydantic import BaseModel, Field


class FbTopicStats(BaseModel):
    entities: List[str]
    emotions_label: str
    topic: str
    sentiment_lab: str
    message: str


class FbTop5TopicStatsRes(BaseModel):
    data: List[FbTopicStats]


class FbIndivAggregatedStats(BaseModel):
    total_likes: int
    count: int


class FbAggregatedStatsRes(BaseModel):
    __root__: List[FbIndivAggregatedStats]
