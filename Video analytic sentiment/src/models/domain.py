from pydantic import BaseModel, HttpUrl
from typing import List, Optional, Dict, Any

class Video(BaseModel):
    """Represents a video being analyzed."""
    url: HttpUrl
    content_summary: Optional[str] = None
    derived_sentiment: Optional[str] = None

class Comment(BaseModel):
    """Represents a single user comment on a video."""
    id: str
    text: str
    analyzed_sentiment: str

class SentimentStatistics(BaseModel):
    """Represents the aggregated sentiment statistics."""
    positive: float
    negative: float
    neutral: float

class KeywordCloudItem(BaseModel):
    """Represents an item in the keyword cloud with its frequency."""
    text: str
    value: int

class AnalysisReport(BaseModel):
    """Represents the comprehensive sentiment analysis report for a video."""
    video: Video
    comments: List[Comment]
    sentiment_statistics: SentimentStatistics
    keyword_cloud: List[KeywordCloudItem]
    conclusion: str
    warnings: List[str]
    topic_sentiments: Dict[str, Any] # Added for topic-specific sentiment