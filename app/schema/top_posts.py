from typing import List, Optional

from pydantic import BaseModel

from .dao import TopPost


##### Top 5 Complaint Comments API & Top 5 Noteworthy Comments API #####
class TopPostsSorted(BaseModel):
    likes: List[TopPost]
    date: List[TopPost]


class TopPostsSortedRes(BaseModel):
    facebook: Optional[TopPostsSorted]
    reddit: Optional[TopPostsSorted]
    twitter: Optional[TopPostsSorted]
    youtube: Optional[TopPostsSorted]
