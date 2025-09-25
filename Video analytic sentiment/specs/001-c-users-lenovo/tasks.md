# Tasks for Video Sentiment Analysis

**Feature**: Sentimental Analysis for a specific video

This document lists the development tasks required to implement the feature. Tasks are ordered by dependency.

## Phase 1: Setup

- **T001: Set up project structure**
  - **File**: N/A (Directory structure)
  - **Action**: Create the `src` and `tests` directories at the root of the project. [X]

- **T002: Create `requirements.txt`**
  - **File**: `requirements.txt`
  - **Action**: Create the file and add the following dependencies:
    ```
    fastapi
    uvicorn
    pydantic
    requests
    yt-dlp
    vaderSentiment
    underthesea
    openai-whisper
    pytest
    ``` [X]

- **T003: Set up logging configuration**
  - **File**: `src/logging_config.py`
  - **Action**: Create a basic logging configuration that can be used across the application. [X]

## Phase 2: Tests (Test-Driven Development)

- **T004: [P] Create contract test for `/analyze` endpoint**
  - **File**: `tests/contract/test_analyze_api.py`
  - **Action**: Create a test that sends a request to the `POST /analyze` endpoint and validates that the response matches the `AnalysisReport` schema in `openapi.yaml`. This test should initially fail. [X]

- **T005: [P] Create integration test for the main user story**
  - **File**: `tests/integration/test_sentiment_analysis.py`
  - **Action**: Create a high-level integration test that simulates the primary user story: providing a URL and getting back a complete analysis report. This test will fail until the final implementation is complete. [X]

## Phase 3: Core Implementation (Models & Services)

- **T006: [P] Create Pydantic models**
  - **File**: `src/models/domain.py`
  - **Action**: Implement the Pydantic models for `Video`, `Comment`, and `AnalysisReport` as defined in `data-model.md`. [X]

- **T007: Create `YouTubeService`**
  - **File**: `src/services/tiktok_service.py`
  - **Action**: Implement a service that uses `yt-dlp` to fetch video information and comments for a given URL. [X]

- **T008: Create `SentimentService`**
  - **File**: `src/services/sentiment_service.py`
  - **Action**: Implement a service that can perform sentiment analysis on a given text, supporting both English (`vaderSentiment`) and Vietnamese (`underthesea`). [X]

- **T009: Create `SpeechToTextService`**
  - **File**: `src/services/speech_to_text_service.py`
  - **Action**: Implement a service that uses `openai-whisper` to transcribe the audio from a downloaded video file. [X]

- **T010: Create `AnalysisService`**
  - **File**: `src/services/analysis_service.py`
  - **Action**: Create the main orchestration service that uses the other services (`YouTubeService`, `SentimentService`, `SpeechToTextService`) to perform the full video analysis. [X]

- **T019: Implement Topic-Specific Sentiment Analysis**
  - **File**: `src/services/analysis_service.py` (or a new service if complexity warrants)
  - **Action**: Enhance the `AnalysisService` (or create a new service) to identify key topics within comments and perform sentiment analysis for each topic, as per FR-008. [X]

- **T013: [P] Add unit tests for services**
  - **File**: `tests/unit/`
  - **Action**: Add unit tests for each of the services (`youtube_service.py`, `sentiment_service.py`, etc.) to ensure they function correctly in isolation. [X]

## Phase 4: API Implementation

- **T011: Implement `/analyze` endpoint**
  - **File**: `src/main.py`
  - **Action**: Create the main FastAPI application and implement the `POST /analyze` endpoint. This endpoint will use the `AnalysisService` to perform the analysis and return the report. This should make the contract test (T004) pass. [X]

## Phase 5: Polish & Finalization

- **T012: Finalize integration test**
  - **File**: `tests/integration/test_sentiment_analysis.py`
  - **Action**: Complete the implementation of the integration test (T005) to ensure it passes. [X]

- **T014: [P] Add documentation**
  - **File**: All new files.
  - **Action**: Add docstrings and type hints to all new functions, classes, and methods. [X] [X]

- **T015: Create CLI interface**
  - **File**: `src/cli/main.py`
  - **Action**: Create a simple command-line interface using a library like `typer` or `argparse` to trigger the analysis from the command line. [X] [X]

- **T018: Create performance validation test**
  - **File**: `tests/performance/test_analysis_speed.py`
  - **Action**: Create a test that downloads a sample video and runs the full analysis, asserting that the total execution time is less than 60 seconds. [X] [X]

## Phase 6: Frontend Implementation

- **T016: [P] Create basic HTML frontend**
  - **File**: `frontend/index.html`
  - **Action**: Create a simple HTML file with a form containing a URL input field and an "Analyze" button. Add a section to display the results. [X] [X]

- **T017: Implement frontend JavaScript**
  - **File**: `frontend/app.js`
  - **Action**: Write JavaScript to:
    1. Fetch the URL from the input field on button click.
    2. Send a POST request to the `/analyze` endpoint.
    3. While waiting for the response, disable the button and input field and show a loading spinner (covers UI-001, UI-002).
    4. Once the response is received, re-enable the form and display the report data in the results section. [X] [X]