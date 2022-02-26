from pydantic import BaseModel, Field
from typing import List
from datetime import datetime
from .py_object_id import PyObjectId


class FbPostRes(BaseModel):
    id: int
    fb_group: str
    created_time: datetime
    message: str
    likes_cnt: int
    comments_cnt: int


class FbDailyStatsRes(BaseModel):
    date: dict
    total_comments: int
    total_likes: int
    count: int
