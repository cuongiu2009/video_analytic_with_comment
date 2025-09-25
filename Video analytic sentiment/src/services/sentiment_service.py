import logging
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from underthesea import sentiment as underthesea_sentiment

logger = logging.getLogger(__name__)

class SentimentService:
    """Service for performing sentiment analysis on text in English and Vietnamese."""
    def __init__(self):
        self.vader_analyzer = SentimentIntensityAnalyzer()
        # underthesea models are typically loaded on first use.
        # We can try to trigger a small analysis to ensure it's ready.
        try:
            underthesea_sentiment("test")
            logger.info("underthesea sentiment model initialized.")
        except Exception as e:
            logger.warning(f"underthesea sentiment model initialization failed: {e}. Vietnamese sentiment analysis might not work.")

    def analyze_english_sentiment(self, text: str) -> str:
        """Analyzes the sentiment of English text using VaderSentiment.

        Args:
            text (str): The English text to analyze.

        Returns:
            str: The sentiment label (Positive, Negative, or Neutral).
        """
        vs = self.vader_analyzer.polarity_scores(text)
        if vs['compound'] >= 0.05:
            return "Positive"
        elif vs['compound'] <= -0.05:
            return "Negative"
        else:
            return "Neutral"

    def analyze_vietnamese_sentiment(self, text: str) -> str:
        """Analyzes the sentiment of Vietnamese text using underthesea.

        Args:
            text (str): The Vietnamese text to analyze.

        Returns:
            str: The sentiment label (Positive, Negative, or Neutral).
        """
        try:
            sentiment_result = underthesea_sentiment(text)
            return sentiment_result[0].capitalize()
        except Exception as e:
            logger.error(f"Error analyzing Vietnamese sentiment with underthesea: {e}")
            return "Neutral" # Fallback to neutral on error

    def analyze_sentiment(self, text: str, lang: str = "en") -> str:
        """Analyzes the sentiment of text, supporting English and Vietnamese.

        Args:
            text (str): The text to analyze.
            lang (str, optional): The language of the text ('en' for English, 'vi' for Vietnamese). Defaults to "en".

        Returns:
            str: The sentiment label (Positive, Negative, or Neutral).
        """
        logger.info(f"Analyzing sentiment for text (lang: {lang}): {text[:50]}...")
        if lang.lower() == "en":
            return self.analyze_english_sentiment(text)
        elif lang.lower() == "vi":
            return self.analyze_vietnamese_sentiment(text)
        else:
            logger.warning(f"Unsupported language for sentiment analysis: {lang}. Defaulting to English.")
            return self.analyze_english_sentiment(text)