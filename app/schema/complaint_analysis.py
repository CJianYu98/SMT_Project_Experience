from typing import Optional

from pydantic import BaseModel


##### Top 20 Complaint API #####
class Top20ComplaintKeywordAnalysisRes(BaseModel):
    word: str
    count: int


##### Complaint Percentage API #####
class ComplaintPercentageRes(BaseModel):
    facebook: Optional[float]
    reddit: Optional[float]
    twitter: Optional[float]
    youtube: Optional[float]
