from typing import Optional

from pydantic import BaseModel


##### Metrics Card Aggregated Statistics (without trend) API #####
class IndivPlatformStat(BaseModel):
    mentions: float
    emotion: Optional[str]


class PlatformMetrics(BaseModel):
    facebook: IndivPlatformStat
    reddit: IndivPlatformStat
    twitter: IndivPlatformStat
    # youtube: IndivPlatformStat


class AggregatedStatsRes(BaseModel):
    posts: int
    comments: int
    likes: int
    platformMetrics: PlatformMetrics


##### Metrics Card Aggregated Statistics (trend) API #####
class TrendStatsRes(BaseModel):
    trend: float


##### Metrics Card Individual Platform Statistics (trend) API #####
class IndivTrendStatsRes(BaseModel):
    facebook: TrendStatsRes
    reddit: TrendStatsRes
    twitter: TrendStatsRes
    youtube: TrendStatsRes
