from typing import List

from pydantic import BaseModel

from .dao import ComplaintOrNotworthyPost


##### Top 5 Noteworthy Comments API #####
class NoteworthyPostsSorted(BaseModel):
    likes: List[ComplaintOrNotworthyPost]
    date: List[ComplaintOrNotworthyPost]


class Top5NoteworthyPostsRes(BaseModel):
    facebook: NoteworthyPostsSorted
    reddit: NoteworthyPostsSorted
    twitter: NoteworthyPostsSorted
    # youtube: NoteworthyPostsSorted
