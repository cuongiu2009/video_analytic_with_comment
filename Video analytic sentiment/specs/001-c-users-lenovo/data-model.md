# Data Model for Video Sentiment Analysis

**Date**: 2025-09-23

This document defines the key data entities for the video sentiment analysis feature, based on the feature specification.

## 1. Video

Represents the video being analyzed.

| Attribute | Type | Description |
|---|---|---|
| `url` | string | The URL of the TikTok video. **(Primary Identifier)** |
| `content_summary` | string | A summary of the video's transcribed content. |
| `derived_sentiment` | string | The overall sentiment derived from the video content (e.g., 'Positive', 'Negative', 'Neutral'). |

## 2. Comment

Represents a single user comment on the video.

| Attribute | Type | Description |
|---|---|---|
| `id` | string | A unique identifier for the comment (provided by the API). **(Primary Identifier)** |
| `text` | string | The text content of the comment. |
| `analyzed_sentiment` | string | The sentiment of the comment ('Positive', 'Negative', 'Neutral'). |

## 3. AnalysisReport

Represents the final analysis report.

| Attribute | Type | Description |
|---|---|---|
| `video` | Video | The video object that was analyzed. |
| `comments` | list[Comment] | A list of the comments that were analyzed. |
| `sentiment_statistics` | object | An object containing the sentiment breakdown (e.g., `{ "positive": 0.7, "negative": 0.2, "neutral": 0.1 }`). |
| `keyword_cloud` | list[object] | A list of keywords and their frequencies (e.g., `[{"text": "love", "value": 50}]`). |
| `conclusion` | string | A summary comparing the video content sentiment with the comment sentiment. |
| `warnings` | list[string] | A list of any warnings generated during the analysis (e.g., incomplete comment list). |

## Relationships

- An `AnalysisReport` is generated for one `Video`.
- A `Video` can have many `Comments`.
- An `AnalysisReport` contains the analysis of many `Comments`.
