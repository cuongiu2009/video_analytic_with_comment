import logging
from typing import List, Dict, Any, Optional
from collections import Counter
import re
import os
import subprocess

from src.models.domain import Video, Comment, AnalysisReport, SentimentStatistics, KeywordCloudItem
from src.services.youtube_service import YouTubeService
from src.services.sentiment_service import SentimentService
from src.services.speech_to_text_service import SpeechToTextService

logger = logging.getLogger(__name__)

class AnalysisService:
    """Orchestrates the video sentiment analysis process."""
    def __init__(self, session_id: str = None):
        self.tiktok_service = TikTokService(session_id=session_id)
        self.sentiment_service = SentimentService()
        self.speech_to_text_service = SpeechToTextService()

    async def analyze_video(self, url: str, content_analysis: bool = True) -> AnalysisReport:
        logger.info(f"Starting analysis for video URL: {url}, content_analysis: {content_analysis}")
        warnings = []

        # 1. Fetch video info and comments
        tiktok_data = await self.tiktok_service.get_video_info_and_comments(url)
        video_info = tiktok_data.get("video_info", {})
        raw_comments = tiktok_data.get("comments", [])

        # 2. Process video content (if requested)
        video_content_summary = None
        video_derived_sentiment = None
        if content_analysis:
            video_path = None
            audio_path = "temp_audio.mp3"
            ffmpeg_exe_path = os.path.join("ffmpeg", "bin", "ffmpeg.exe")

            if not os.path.exists(ffmpeg_exe_path):
                warnings.append("ffmpeg.exe not found in the project's ffmpeg/bin directory. Cannot analyze video content.")
            else:
                try:
                    # Download the video file
                    video_path = await self.tiktok_service.download_video(url, "temp_video.mp4")

                    if video_path and video_path != "dummy_video.mp4": # Check if a real path was returned
                        logger.info(f"Extracting audio from {video_path} using ffmpeg.")
                        command = [
                            ffmpeg_exe_path,
                            '-i', video_path,
                            '-y', # Overwrite output file if it exists
                            '-q:a', '0', # Best audio quality
                            '-map', 'a', # Select only audio stream
                            audio_path
                        ]
                        subprocess.run(command, check=True, capture_output=True, text=True)

                        transcription = self.speech_to_text_service.transcribe_audio(audio_path)
                        video_content_summary = transcription[:200] + "..." if len(transcription) > 200 else transcription
                        video_derived_sentiment = self.sentiment_service.analyze_sentiment(transcription, lang="en")

                        # Clean up temporary files
                        if os.path.exists(video_path): os.remove(video_path)
                        if os.path.exists(audio_path): os.remove(audio_path)

                    else:
                        warnings.append("Video content could not be analyzed: Video download failed or was skipped.")
                except subprocess.CalledProcessError as e:
                    logger.error(f"ffmpeg failed during audio extraction: {e.stderr}")
                    warnings.append("Failed to extract audio from video using ffmpeg.")
                except Exception as e:
                    logger.error(f"Error during video content analysis: {e}", exc_info=True)
                    warnings.append("Video content could not be analyzed due to an error.")
        else:
            warnings.append("Video content analysis was skipped as requested.")
        # 3. Analyze comments
        analyzed_comments: List[Comment] = []
        sentiment_counts = Counter()
        all_comment_words = []

        if not raw_comments:
            warnings.append("No comments found for this video.")
        else:
            for raw_comment in raw_comments:
                comment_text = raw_comment.get("text", "")
                comment_id = raw_comment.get("id", "")
                
                # Determine language for sentiment analysis (simplified for now)
                # In a real app, you'd use a language detection library
                lang = "en" # Default to English
                # Simple heuristic: if Vietnamese characters are present, assume Vietnamese
                if re.search(r'[àáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđ]', comment_text, re.IGNORECASE):
                    lang = "vi"

                sentiment = self.sentiment_service.analyze_sentiment(comment_text, lang=lang)
                analyzed_comments.append(Comment(id=comment_id, text=comment_text, analyzed_sentiment=sentiment))
                sentiment_counts[sentiment.lower()] += 1

                # For word cloud
                words = re.findall(r'\b\w+\b', comment_text.lower())
                all_comment_words.extend([word for word in words if len(word) > 2 and word not in self._get_stopwords(lang)])

        # 4. Calculate sentiment statistics
        total_comments = len(analyzed_comments)
        sentiment_stats = SentimentStatistics(
            positive=sentiment_counts["positive"] / total_comments if total_comments else 0,
            negative=sentiment_counts["negative"] / total_comments if total_comments else 0,
            neutral=sentiment_counts["neutral"] / total_comments if total_comments else 0,
        )

        # 5. Generate keyword cloud
        word_freq = Counter(all_comment_words)
        keyword_cloud = [KeywordCloudItem(text=word, value=count) for word, count in word_freq.most_common(10)]

        # 6. Implement Topic-Specific Sentiment Analysis (Placeholder)
        topic_sentiments = self._analyze_topic_sentiments(analyzed_comments)

        # 7. Generate conclusion (simplified)
        conclusion = self._generate_conclusion(video_derived_sentiment, sentiment_stats)

        # 8. Construct report
        video_model = Video(
            url=url,
            content_summary=video_content_summary,
            derived_sentiment=video_derived_sentiment
        )

        report = AnalysisReport(
            video=video_model,
            comments=analyzed_comments,
            sentiment_statistics=sentiment_stats,
            keyword_cloud=keyword_cloud,
            conclusion=conclusion,
            warnings=warnings,
            topic_sentiments=topic_sentiments # Add topic sentiments to report
        )
        logger.info(f"Analysis complete for {url}")
        return report

    def _get_stopwords(self, lang: str) -> List[str]:
        # Placeholder for stopwords. In a real app, load from a file or library.
        if lang == "en":
            return ["the", "a", "an", "is", "it", "of", "to", "and", "in", "for", "this", "that"]
        elif lang == "vi":
            return ["là", "một", "cái", "của", "và", "trong", "cho", "này", "đó"]
        return []

    def _analyze_topic_sentiments(self, comments: List[Comment]) -> Dict[str, Any]:
        # Placeholder for topic modeling and sentiment analysis per topic
        logger.warning("Topic-specific sentiment analysis is a placeholder and not fully implemented.")
        # In a real implementation, you would:
        # 1. Preprocess comments (tokenization, lemmatization)
        # 2. Apply topic modeling (e.g., LDA, NMF) to extract topics
        # 3. Assign comments to topics
        # 4. Perform sentiment analysis for comments within each topic
        return {"placeholder_topic": {"sentiment": "neutral", "count": len(comments)}}

    def _generate_conclusion(self, video_sentiment: Optional[str], comment_stats: SentimentStatistics) -> str:
        if video_sentiment and comment_stats.positive > comment_stats.negative:
            return f"The video content is {video_sentiment.lower()} and the comments are generally positive."
        elif video_sentiment and comment_stats.negative > comment_stats.positive:
            return f"The video content is {video_sentiment.lower()} but the comments lean negative."
        elif video_sentiment:
            return f"The video content is {video_sentiment.lower()} and comments are mixed/neutral."
        else:
            return "Comment sentiment analysis complete. Video content sentiment was not available."