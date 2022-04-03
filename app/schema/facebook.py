from typing import List

from pydantic import BaseModel


class FbTopicStats(BaseModel):
    entities: List[str]
    emotions_label: str
    topic: str
    sentiment_lab: str
    message: str


class FbTop5TopicStatsRes(BaseModel):
    data: List[FbTopicStats]


class FbEmotionCount(BaseModel):
    emotion: str
    count: int


class FbIndivAggregatedStatsRes(BaseModel):
    total_likes: int
    count: int
    emotion_counts: List[FbEmotionCount]


class FbTrendStatsRes(BaseModel):
    count: int


class FbKeywordAnalysis(BaseModel):
    entities: List[str]
    sentiment_label: str


class FbKeywordAnalysisRes(BaseModel):
    data: List[FbKeywordAnalysis]


class FbComplaintTopKeywordsAnalysis(BaseModel):
    entities: List[str]


class FbComplaintTopKeywordsAnalysisRes(BaseModel):
    data: List[FbComplaintTopKeywordsAnalysis]
