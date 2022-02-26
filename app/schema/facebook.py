from pydantic import BaseModel
from typing import List
from datetime import datetime

class FbPost(BaseModel):
    _id: int
    fb_group: str
    created_time: str
    message: str
    likes_cnt: int
    comments_cnt: int


class FbPostRes(BaseModel):
    code: int
    datetime: datetime
    data: List[FbPost]