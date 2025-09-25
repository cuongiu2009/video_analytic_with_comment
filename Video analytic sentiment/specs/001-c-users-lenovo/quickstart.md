# Quickstart Guide: Video Sentiment Analysis

**Date**: 2025-09-23

This guide provides instructions on how to set up the environment and run the video sentiment analysis application.

## 1. Prerequisites

- Python 3.11+
- `pip` for package installation

## 2. Setup

1.  **Clone the repository** (if you haven't already).

2.  **Create a virtual environment**:
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows, use `.venv\Scripts\activate`
    ```

3.  **Install dependencies**:
A `requirements.txt` file will be created during the implementation phase. Once it is available, run:
    ```bash
    pip install -r requirements.txt
    ```

## 3. Running the Application

The application will be served via a FastAPI server.

1.  **Start the server**:
    ```bash
    uvicorn src.main:app --reload
    ```

2.  **Access the API**:
The API will be available at `http://127.0.0.1:8000`.

## 4. Running the Analysis

You can send a POST request to the `/analyze` endpoint to start an analysis.

**Example using `curl`**:

```bash
curl -X POST "http://127.0.0.1:8000/analyze" \
-H "Content-Type: application/json" \
-d '{
  "url": "<URL_OF_TIKTOK_VIDEO>",
  "content_analysis": true
}'
```

## 5. Running Tests

To run the test suite, use `pytest`:

```bash
pytest
```
