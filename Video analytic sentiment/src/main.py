from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, HttpUrl
from src.services.analysis_service import AnalysisService
from src.models.domain import AnalysisReport
from src.logging_config import setup_logging
import logging
from fastapi.middleware.cors import CORSMiddleware
import os

from src.services.analysis_service import AnalysisService
from src.logging_config import setup_logging

# Setup logging as the very first thing
setup_logging()
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Video Sentiment Analysis API",
    description="API for analyzing sentiment of YouTube videos and their comments.",
    version="1.0.0"
)

# Add CORS middleware to allow frontend to access the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

class AnalyzeRequest(BaseModel):
    url: HttpUrl
    content_analysis: bool = True

@app.post("/analyze", response_model=AnalysisReport)
async def analyze_video_endpoint(request: AnalyzeRequest):
    logger.info(f"Received analysis request for URL: {request.url}, content_analysis: {request.content_analysis}")
    analysis_service = AnalysisService()
    try:
        report = await analysis_service.analyze_video(str(request.url), request.content_analysis)
        return report
    except Exception as e:
        logger.error(f"Error during video analysis for {request.url}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")

@app.get("/health")
async def health_check():
    return {"status": "ok"}