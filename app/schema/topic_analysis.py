from typing import List, Optional

from pydantic import BaseModel, Field


class SentimentStats(BaseModel):
    sentiment: str
    count: int


class EmotionStats(BaseModel):
    emotion: str
    count: int


class IndiTopicStats(BaseModel):
    name: str
    topThreeMentions: List[str] = []
    mentions: int
    sentiment: List[SentimentStats]
    emotions: List[EmotionStats]


class Top5TopicStatsRes(BaseModel):
    __root__: List[IndiTopicStats]
