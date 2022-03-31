from typing import List

from pydantic import BaseModel

class AggregatedStatsRes(BaseModel):
    posts: int
    likes: int
    platformMetrics: dict
