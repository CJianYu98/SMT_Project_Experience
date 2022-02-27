from pydantic import BaseModel, Field
from typing import List
from datetime import datetime


class FbPostRes(BaseModel):
    id: int
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