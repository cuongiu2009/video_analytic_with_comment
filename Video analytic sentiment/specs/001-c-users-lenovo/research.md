# Research for Video Sentiment Analysis

**Date**: 2025-09-23

This document outlines the technology choices for the video sentiment analysis feature.

## TikTok Comment Scraping

- **Decision**: `TikTokApi`
- **Rationale**: This unofficial Python library provides a convenient wrapper around TikTok's internal APIs, simplifying the process of fetching video information and comments. It is free and actively maintained. While direct scraping or using `Selenium` are alternatives, they add significant complexity. Paid APIs are not considered for this initial version.
- **Alternatives considered**: `requests` + direct API calls, `Selenium`, paid scraping services.

## Sentiment Analysis

### English
- **Decision**: `vaderSentiment`
- **Rationale**: VADER (Valence Aware Dictionary and sEntiment Reasoner) is specifically tuned for sentiments expressed in social media, which makes it a perfect fit for analyzing TikTok comments. It is simple to use and provides a polarity score (positive/negative/neutral).
- **Alternatives considered**: `TextBlob`, `NLTK`.

### Vietnamese
- **Decision**: `underthesea`
- **Rationale**: This is a comprehensive, open-source NLP toolkit specifically for the Vietnamese language. It is the clear choice for this task as it provides a dedicated sentiment analysis module.
- **Alternatives considered**: None, this is the standard for Vietnamese NLP in Python.

## Speech-to-Text

- **Decision**: `openai-whisper`
- **Rationale**: Whisper provides state-of-the-art accuracy for speech-to-text and has excellent multilingual capabilities, including robust support for both English and Vietnamese. Its ability to handle accents and background noise makes it ideal for analyzing real-world video content.
- **Alternatives considered**: `Vosk` (offline), Google Cloud Speech-to-Text, AssemblyAI.

## Web Framework / API

- **Decision**: `FastAPI`
- **Rationale**: FastAPI is a modern, high-performance web framework for Python that is easy to learn and use. It's perfect for creating the simple API endpoint that will be needed to trigger the analysis.
- **Alternatives considered**: `Flask`, `Django`.
