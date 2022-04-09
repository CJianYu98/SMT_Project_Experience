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


##### Trend Data Plot API #####
class TrendPlotData(BaseModel):
    date: datetime
    mentions: int
    likes: int
    positive_sentiment: int
    negative_sentiment: int
    neutral_sentiment: int
    anger_emotion: int
    fear_emotion: int
    joy_emotion: int
    sadness_emotion: int
    neutral_emotion: int
    awards: Optional[int]
    retweets: Optional[int]
    views: Optional[int]


class TrendPlotDataRes(BaseModel):
    data: List[TrendPlotData]


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
class ComplaintOrNotworthyPost(BaseModel):
    likes: int
    datetime: datetime
    comment: str
    topic: str
    sentiment: str
    emotion: str
    link: Optional[str]
    thumbnail: Optional[str]
    intent: Optional[str]
    link: Optional[str]
    img: Optional[str]


class Top5ComplaintOrNoteworthyPostsRes(BaseModel):
    data: List[ComplaintOrNotworthyPost]
