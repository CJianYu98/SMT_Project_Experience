from typing import List

from pydantic import BaseModel

from .dao import ComplaintOrNotworthyPost

##### Top 20 Complaint API #####
class Top20ComplaintKeywordAnalysisRes(BaseModel):
    word: str
    count: int


##### Top 5 Complaint Comments API & Top 5 Noteworthy Comments API #####
class ComplaintOrNoteworthyPostsSorted(BaseModel):
    likes: List[ComplaintOrNotworthyPost]
    date: List[ComplaintOrNotworthyPost]


class Top5ComplaintOrNoteworthyPostsRes(BaseModel):
    facebook: ComplaintOrNoteworthyPostsSorted
    reddit: ComplaintOrNoteworthyPostsSorted
    twitter: ComplaintOrNoteworthyPostsSorted
    # youtube: ComplaintOrNoteworthyCommentsSorted
