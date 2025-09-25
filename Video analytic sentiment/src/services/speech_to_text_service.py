import logging
import whisper
import os

logger = logging.getLogger(__name__)

class SpeechToTextService:
    """Service for performing speech-to-text transcription using OpenAI Whisper."""
    def __init__(self):
        # Load the Whisper model. This can be a large download.
        # For initial setup, we might use a smaller model or a placeholder.
        # 'base' is a good balance for many cases.
        try:
            self.model = whisper.load_model("base")
            logger.info("Whisper 'base' model loaded successfully.")
        except Exception as e:
            logger.error(f"Could not load Whisper model: {e}. Transcription will be a placeholder.")
            self.model = None

    def transcribe_audio(self, audio_path: str) -> str:
        """Transcribes audio from a given audio file path.

        Args:
            audio_path (str): The path to the audio file.

        Returns:
            str: The transcribed text, or an empty string/placeholder if transcription fails.
        """
        if not os.path.exists(audio_path):
            logger.error(f"Audio file not found: {audio_path}")
            return ""

        if self.model:
            logger.info(f"Transcribing audio from: {audio_path}")
            try:
                result = self.model.transcribe(audio_path)
                return result["text"]
            except Exception as e:
                logger.error(f"Error during transcription of {audio_path}: {e}")
                return ""
        else:
            logger.warning("Whisper model not loaded. Returning placeholder transcription.")
            return "This is a placeholder transcription of the video content."