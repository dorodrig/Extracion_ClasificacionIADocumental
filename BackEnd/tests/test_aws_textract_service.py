import pytest
from unittest.mock import patch, MagicMock
from app.services.aws_textract_service import AWSTextractService

@pytest.fixture
def mock_boto3_client():
    with patch('app.services.aws_textract_service.boto3.client') as mock_client:
        yield mock_client

def test_process_page_bytes_success(mock_boto3_client):
    # Setup
    mock_instance = MagicMock()
    mock_boto3_client.return_value = mock_instance
    mock_instance.detect_document_text.return_value = {"Blocks": [{"BlockType": "LINE", "Text": "Test", "Confidence": 99.0}]}
    
    # Execution
    service = AWSTextractService()
    result = service.process_page_bytes(b"test_bytes")
    
    # Assert
    assert "Blocks" in result
    assert result["Blocks"][0]["Text"] == "Test"
    assert "__elapsed_ms" in result
    mock_instance.detect_document_text.assert_called_once()

def test_process_page_bytes_analyze_document(mock_boto3_client):
    # Setup
    mock_instance = MagicMock()
    mock_boto3_client.return_value = mock_instance
    mock_instance.analyze_document.return_value = {"Blocks": []}
    
    # Execution
    service = AWSTextractService()
    result = service.process_page_bytes(b"test_bytes", use_analyze=True)
    
    # Assert
    mock_instance.analyze_document.assert_called_once()

@patch('app.services.aws_textract_service.time.sleep', return_value=None)
def test_process_page_bytes_retry(mock_sleep, mock_boto3_client):
    # Setup
    mock_instance = MagicMock()
    mock_boto3_client.return_value = mock_instance
    
    # Fail 2 times, succeed on 3rd
    mock_instance.detect_document_text.side_effect = [
        Exception("Timeout 1"),
        Exception("Timeout 2"),
        {"Blocks": []}
    ]
    
    # Execution
    service = AWSTextractService()
    result = service.process_page_bytes(b"test_bytes")
    
    # Assert
    assert mock_instance.detect_document_text.call_count == 3
    assert mock_sleep.call_count == 2
    assert "Blocks" in result
