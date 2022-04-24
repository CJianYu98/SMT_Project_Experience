import re
from typing import List, Optional

from pydantic import BaseModel, Field, validator


class Filter(BaseModel):
    endDate: str
    numDays: int
    platforms: List[str]
    sentiments: List[str]
    emotions: List[str]
    query: Optional[str] = Field(...)
    interval: Optional[str]
    topN: Optional[int]
    postType: Optional[str]

    @validator("endDate")
    def check_datetime_str_format(cls, v):
        pattern = re.compile("\d\d\d\d-\d\d-\d\d")
        if not pattern.fullmatch(v):
            raise ValueError("Datetime string not in the correct format")
        return v

    @validator("numDays")
    def check_numDays(cls, v):
        if v <= 0:
            raise ValueError("Num days should not be negative integer")
        return v

    @validator("platforms")
    def check_platforms(cls, v):
        PLATFORMS = ["facebook", "reddit", "twitter", "youtube"]
        if set(v).difference(set(PLATFORMS)):
            raise ValueError("Invalid platform value")
        return v

    @validator("sentiments")
    def check_sentiments(cls, v):
        SENTIMENTS = ["positive", "neutral", "negative"]
        if set(v).difference(set(SENTIMENTS)):
            raise ValueError("Invalid sentiment value")
        return v

    @validator("emotions")
    def check_emotions(cls, v):
        EMOTIONS = ["anger", "fear", "joy", "neutral", "sadness"]
        if set(v).difference(set(EMOTIONS)):
            raise ValueError("Invalid emotion value")
        return v

    @validator("interval")
    def check_interval(cls, v):
        INTERVALS = ["3hours", "daily", "weekly", "monthly", "yearly"]
        if v not in INTERVALS:
            raise ValueError("Invalid interval string value")
        return v
    
    @validator("postType")
    def check_post_type(cls, v):
        POST_TYPES = ["all", "complaint", "noteworthy"]
        if v not in POST_TYPES:
            raise ValueError("Invalid post type string value")
        return v