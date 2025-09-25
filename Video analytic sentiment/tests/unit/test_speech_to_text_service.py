import pytest
from unittest.mock import MagicMock, patch
from src.services.speech_to_text_service import SpeechToTextService
import os

@pytest.fixture
def speech_to_text_service():
    # Mock whisper.load_model to prevent actual model loading during tests
    with patch('whisper.load_model') as mock_load_model:
        mock_model = MagicMock()
        mock_load_model.return_value = mock_model
        service = SpeechToTextService()
        service.model = mock_model # Ensure the service uses our mock
        yield service

def test_transcribe_audio_success(speech_to_text_service):
    # Mock os.path.exists to simulate a valid audio file
    with patch('os.path.exists', return_value=True):
        mock_audio_path = "/fake/path/audio.mp3"
        expected_transcription = "This is a test transcription."
        
        # Configure the mock model's transcribe method
        speech_to_text_service.model.transcribe.return_value = {"text": expected_transcription}
        
        result = speech_to_text_service.transcribe_audio(mock_audio_path)
        assert result == expected_transcription
        speech_to_text_service.model.transcribe.assert_called_once_with(mock_audio_path)

def test_transcribe_audio_file_not_found(speech_to_text_service):
    # Mock os.path.exists to simulate a missing audio file
    with patch('os.path.exists', return_value=False):
        mock_audio_path = "/fake/path/non_existent.mp3"
        result = speech_to_text_service.transcribe_audio(mock_audio_path)
        assert result == ""
        speech_to_text_service.model.transcribe.assert_not_called()

def test_transcribe_audio_model_not_loaded():
    # Test scenario where model failed to load during __init__
    with patch('whisper.load_model', side_effect=Exception("Model load error")):
        service = SpeechToTextService()
        assert service.model is None
        
        with patch('os.path.exists', return_value=True):
            mock_audio_path = "/fake/path/audio.mp3"
            result = service.transcribe_audio(mock_audio_path)
            assert result == "This is a placeholder transcription of the video content."

def test_transcribe_audio_transcription_error(speech_to_text_service):
    with patch('os.path.exists', return_value=True):
        mock_audio_path = "/fake/path/error_audio.mp3"
        speech_to_text_service.model.transcribe.side_effect = Exception("Transcription failed")
        
        result = speech_to_text_service.transcribe_audio(mock_audio_path)
        assert result == ""
        speech_to_text_service.model.transcribe.assert_called_once_with(mock_audio_path)
