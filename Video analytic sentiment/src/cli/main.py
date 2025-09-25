import typer
import asyncio
import json
from typing_extensions import Annotated
import os

from src.services.analysis_service import AnalysisService
from src.logging_config import setup_logging

# Setup logging as the very first thing
setup_logging()

app = typer.Typer(
    name="video-sentiment-cli",
    help="CLI for analyzing sentiment of YouTube videos and their comments."
)

@app.command(
    name="analyze",
    help="Analyze a YouTube video URL and generate a sentiment report."
)
def analyze_video_cli(
    url: Annotated[str, typer.Argument(help="The URL of the YouTube video to analyze.")],
    content_analysis: Annotated[bool, typer.Option(
        "--content-analysis/--no-content-analysis",
        help="Whether to perform content analysis on the video (speech-to-text, etc.).",
        rich_help_panel="Analysis Options"
    )] = True,
):
    """Analyze a YouTube video URL and generate a sentiment report."""
    typer.echo(f"Starting analysis for URL: {url}")
    typer.echo(f"Content analysis enabled: {content_analysis}")

    analysis_service = AnalysisService()
    try:
        report = asyncio.run(analysis_service.analyze_video(url, content_analysis))
        typer.echo("\n--- Analysis Report ---")
        typer.echo(json.dumps(report.model_dump(), indent=2, ensure_ascii=False))
        typer.echo("\nAnalysis complete.")
    except Exception as e:
        typer.echo(f"\nError during analysis: {e}", err=True)
        raise typer.Exit(code=1)

if __name__ == "__main__":
    app()