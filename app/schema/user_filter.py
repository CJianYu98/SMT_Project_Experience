from pydantic import BaseModel, validator, Field
from typing import List, Optional
import re

class Filter(BaseModel):
    endDate: str
    numDays: int
    platforms: List[str]
    sentiments: List[str]
    emotions: List[str]
    query: Optional[str] = Field(...)

    @validator('endDate')
    def check_datetime_str_format(cls, v):
        pattern = re.compile("\d\d\d\d-\d\d-\d\d")
        if not pattern.fullmatch(v):
            raise ValueError("Datetime string not in the correct format")
        return v

    @validator('numDays')
    def check_numDays(cls, v):
        if v <= 0:
            raise ValueError("Num days should not be negative integer")
        return v

    @validator(('platforms'))
    def check_platforms(cls, v):
        PLATFORMS = ['Facebook', 'Reddit', 'Twitter', 'Youtube']
        if set(v).difference(set(PLATFORMS)):
            raise ValueError("Invalid platform value")
        return v

    @validator(('sentiments'))
    def check_sentiments(cls, v):
        SENTIMENTS = ['positive', 'neutral', 'negative']
        if set(v).difference(set(SENTIMENTS)):
            raise ValueError("Invalid sentiment value")
        return v
    
    @validator(('emotions'))
    def check_emotions(cls, v):
        EMOTIONS = ['anger', 'fear', 'joy', 'neutral', 'sadness']
        if set(v).difference(set(EMOTIONS)):
            raise ValueError("Invalid emotion value")
        return v