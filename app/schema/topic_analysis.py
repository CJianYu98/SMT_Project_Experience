from typing import List

from pydantic import BaseModel

##### Top 5 Topics Stats API #####
class SentimentStats(BaseModel):
    sentiment: str
    count: int


class EmotionStats(BaseModel):
    emotion: str
    count: int


class IndiTopicStatsRes(BaseModel):
    name: str
    topThreeMentions: List[str] = []
    mentions: int
    sentiment: List[SentimentStats]
    emotions: List[EmotionStats]

