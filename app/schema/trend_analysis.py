from typing import List

from pydantic import BaseModel

class AggregatedStatsRes(BaseModel):
    posts: int
    comments: int
    likes: int
    platformMetrics: dict


class TrendStatsRes(BaseModel):
    trend: float


class IndivTrendStatsRes(BaseModel):
    Facebook: TrendStatsRes
    Reddit: TrendStatsRes
    Twitter: TrendStatsRes
    Youtube: TrendStatsRes