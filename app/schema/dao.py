from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


##### Top 5 Topics Stats API #####
class TopicStats(BaseModel):
    entities: List[str]
    emotions_label: str
    topic: str
    sentiment_label: str
    text: str


class Top5TopicStatsRes(BaseModel):
    data: List[TopicStats]


##### Metrics Card Aggregated Statistics (without trend) API #####
class EmotionCount(BaseModel):
    emotion: str
    count: int


class AggregatedStatsRes(BaseModel):
    total_likes: int
    count: int
    emotion_counts: List[EmotionCount]


##### Metrics Card Aggregated Statistics (trend) API & Metrics Card Individual Platform Statistics (trend) API #####
class TrendStatsRes(BaseModel):
    count: int


##### Top 20 Keywords API #####
class KeywordStats(BaseModel):
    entities: List[str]
    sentiment_label: str


class KeywordAnalysisRes(BaseModel):
    data: List[KeywordStats]


##### Top 20 Complaint API #####
class ComplaintTopKeywordsEntities(BaseModel):
    entities: List[str]


class ComplaintTopKeywordsAnalysisRes(BaseModel):
    data: List[ComplaintTopKeywordsEntities]


##### Top 5 Complaint Comments API & Top 5 Noteworthy Comments API #####
class ComplaintOrNotworthyComment(BaseModel):
    likes: int
    datetime: datetime
    comment: str
    topic: list
    sentiment: str
    emotion: str
    intent: Optional[str]
    link: Optional[str]
    img: Optional[str]


class Top5ComplaintOrNoteworthyCommentsRes(BaseModel):
    data: List[ComplaintOrNotworthyComment]
