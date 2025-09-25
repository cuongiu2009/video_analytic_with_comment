import pytest
from unittest.mock import patch, MagicMock
from src.services.sentiment_service import SentimentService

# Module-level patch for underthesea.sentiment
@pytest.fixture(autouse=True)
def mock_underthesea_sentiment_module():
    with patch('src.services.sentiment_service.underthesea_sentiment') as mock_sentiment:
        mock_sentiment.return_value = ('neutral', 0.5) # Default mock return
        yield mock_sentiment

@pytest.fixture
def sentiment_service():
    return SentimentService()

def test_analyze_english_sentiment_positive(sentiment_service):
    text = "This is a fantastic movie! I loved it."
    assert sentiment_service.analyze_english_sentiment(text) == "Positive"

def test_analyze_english_sentiment_negative(sentiment_service):
    text = "This is a terrible movie. I hated it."
    assert sentiment_service.analyze_english_sentiment(text) == "Negative"

def test_analyze_english_sentiment_neutral(sentiment_service):
    text = "This is a neutral statement."
    assert sentiment_service.analyze_english_sentiment(text) == "Neutral"

def test_analyze_vietnamese_sentiment_positive(mock_underthesea_sentiment_module, sentiment_service):
    mock_underthesea_sentiment_module.return_value = ('positive', 0.9)
    text = "Phim này rất hay! Tôi rất thích."
    assert sentiment_service.analyze_vietnamese_sentiment(text) == "Positive"

def test_analyze_vietnamese_sentiment_negative(mock_underthesea_sentiment_module, sentiment_service):
    mock_underthesea_sentiment_module.return_value = ('negative', 0.8)
    text = "Phim này dở tệ. Tôi ghét nó."
    assert sentiment_service.analyze_vietnamese_sentiment(text) == "Negative"

def test_analyze_vietnamese_sentiment_neutral(mock_underthesea_sentiment_module, sentiment_service):
    mock_underthesea_sentiment_module.return_value = ('neutral', 0.5)
    text = "Phim này cũng được. Không có gì đặc biệt."
    assert sentiment_service.analyze_vietnamese_sentiment(text) == "Neutral"

def test_analyze_sentiment_default_english(sentiment_service):
    text = "Great product!"
    assert sentiment_service.analyze_sentiment(text) == "Positive"

def test_analyze_sentiment_vietnamese_explicit(mock_underthesea_sentiment_module, sentiment_service):
    mock_underthesea_sentiment_module.return_value = ('positive', 0.9)
    text = "Sản phẩm tuyệt vời!"
    assert sentiment_service.analyze_sentiment(text, lang="vi") == "Positive"

def test_analyze_sentiment_unsupported_language(sentiment_service):
    text = "Hola mundo!"
    # Should default to English and return neutral for this text
    assert sentiment_service.analyze_sentiment(text, lang="es") == "Neutral"