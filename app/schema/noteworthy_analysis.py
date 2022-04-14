from typing import List, Optional

from pydantic import BaseModel

from .dao import ComplaintOrNotworthyPost


##### Top 5 Noteworthy Comments API #####
class NoteworthyPostsSorted(BaseModel):
    likes: List[ComplaintOrNotworthyPost]
    date: List[ComplaintOrNotworthyPost]


class Top5NoteworthyPostsRes(BaseModel):
    facebook: Optional[NoteworthyPostsSorted]
    reddit: Optional[NoteworthyPostsSorted]
    twitter: Optional[NoteworthyPostsSorted]
    youtube: Optional[NoteworthyPostsSorted]
