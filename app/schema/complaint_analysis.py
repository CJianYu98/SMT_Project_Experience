from typing import List

from pydantic import BaseModel

from .dao import ComplaintOrNotworthyPost

##### Top 20 Complaint API #####
class Top20ComplaintKeywordAnalysisRes(BaseModel):
    word: str
    count: int


##### Top 5 Complaint Comments API & Top 5 Noteworthy Comments API #####
class ComplaintPostsSorted(BaseModel):
    likes: List[ComplaintOrNotworthyPost]
    date: List[ComplaintOrNotworthyPost]


class Top5ComplaintPostsRes(BaseModel):
    facebook: ComplaintPostsSorted
    reddit: ComplaintPostsSorted
    twitter: ComplaintPostsSorted
    youtube: ComplaintPostsSorted


##### Complaint Percentage API #####
class ComplaintPercentageRes(BaseModel):
    facebook: float
    reddit: float
    twitter: float
    youtube: float
