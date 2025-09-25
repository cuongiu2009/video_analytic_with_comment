import pytest
import time
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_analysis_speed():
    """Tests that the /analyze endpoint responds within the performance goal (60 seconds)."""
    # NOTE: This performance test currently measures the speed of the internal logic
    # and mocked external services. For a true end-to-end performance test,
    # actual TikTok API calls and Whisper transcription would need to be unmocked
    # or simulated more realistically.

    test_url = "https://www.tiktok.com/@tiktok/video/7283180000000000000" # Dummy URL
    start_time = time.time()

    response = client.post(
        "/analyze",
        json={
            "url": test_url,
            "content_analysis": True
        }
    )

    end_time = time.time()
    elapsed_time = end_time - start_time

    assert response.status_code == 200
    assert elapsed_time < 60, f"Analysis took too long: {elapsed_time:.2f} seconds"

    report = response.json()
    assert "video" in report
    assert "comments" in report
    assert "sentiment_statistics" in report