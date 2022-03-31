from pydantic import BaseModel, Field
from typing import List
from datetime import datetime


class FbPostRes(BaseModel):
    id: int
    object_id: str
    fb_group: str
    created_time: datetime
    message: str
    likes_cnt: int
    comments_cnt: int


class FbStatsRes(BaseModel):
    date: dict
    total_comments: int
    total_likes: int
    count: int

class FbTrendRes(BaseModel):
    perc_change: float

class FbTopicStats(BaseModel):
    entities: List[str]
    emotions_label: str
    topic: str
    sentiment_lab: str
    message: str

class FbTop5TopicStatsRes(BaseModel):
    data: List[FbTopicStats]