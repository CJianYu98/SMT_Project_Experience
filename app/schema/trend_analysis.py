from typing import Optional, List

from pydantic import BaseModel


##### Metrics Card Aggregated Statistics (without trend) API #####
class IndivPlatformStat(BaseModel):
    mentions: float
    emotion: Optional[str]


class PlatformMetrics(BaseModel):
    facebook: Optional[IndivPlatformStat]
    reddit: Optional[IndivPlatformStat]
    twitter: Optional[IndivPlatformStat]
    youtube: Optional[IndivPlatformStat]


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
    facebook: Optional[TrendStatsRes]
    reddit: Optional[TrendStatsRes]
    twitter: Optional[TrendStatsRes]
    youtube: Optional[TrendStatsRes]


##### Trend Data Plot API #####
class SentimentTrendPlotData(BaseModel):
    positive: List[int]
    neutral: List[int]
    negative: List[int]


class EmotionTrendPlotData(BaseModel):
    anger: List[int]
    fear: List[int]
    joy: List[int]
    anger: List[int]
    neutral: List[int]


class StandardTrendPlotData(BaseModel):
    mentions: List[int]
    likes: List[int]
    sentiments: SentimentTrendPlotData
    emotions: EmotionTrendPlotData


class RedditTrendPlotData(StandardTrendPlotData):
    awards: List[int]


class TwitterTrendPlotData(StandardTrendPlotData):
    retweets: List[int]


class YoutubeTrendPlotData(StandardTrendPlotData):
    views: List[int]


class TrendPlotDataRes(BaseModel):
    facebook: StandardTrendPlotData
    reddit: RedditTrendPlotData
    twitter: TwitterTrendPlotData
    youtube: YoutubeTrendPlotData