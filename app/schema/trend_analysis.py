from typing import Optional, List

from pydantic import BaseModel


##### Metrics Card Aggregated Statistics (without trend) API #####
class IndivPlatformStat(BaseModel):
    mentions: Optional[float]
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
    sadness: List[int]
    neutral: List[int]


class StandardTrendPlotData(BaseModel):
    dates: List[str]
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


# ##### Social Media Feed Stats API #####
class SentimentCount(BaseModel):
    sentiment: str
    count: int


class EmotionCount(BaseModel):
    emotion: str
    count: int

class IndivSocialMediaFeedAggregatedStats(BaseModel):
    mentions: int
    sentiment: List[SentimentCount]
    emotions: List[EmotionCount]


class SocialMediaFeedAggregatedStatsRes(BaseModel):
    facebook: Optional[IndivSocialMediaFeedAggregatedStats]
    reddit: Optional[IndivSocialMediaFeedAggregatedStats]
    twitter: Optional[IndivSocialMediaFeedAggregatedStats]
    youtube: Optional[IndivSocialMediaFeedAggregatedStats]