from typing import List

from pydantic import BaseModel

from .dao import ComplaintOrNotworthyComment


##### Top 20 Complaint API #####
class Top20ComplaintKeywordAnalysisRes(BaseModel):
    word: str
    count: int


##### Top 5 Complaint Comments API & Top 5 Noteworthy Comments API #####
class ComplaintOrNoteworthyCommentsSorted(BaseModel):
    likes: List[ComplaintOrNotworthyComment]
    date: List[ComplaintOrNotworthyComment]


class Top5ComplaintOrNoteworthyCommentsRes(BaseModel):
    facebook: ComplaintOrNoteworthyCommentsSorted
    # reddit: ComplaintOrNoteworthyCommentsSorted
    # twitter: ComplaintOrNoteworthyCommentsSorted
    # youtube: ComplaintOrNoteworthyCommentsSorted
