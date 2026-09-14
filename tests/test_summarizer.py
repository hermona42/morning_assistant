import pytest
from unittest.mock import patch, MagicMock


def test_generate_morning_brief_returns_html_str():
    """
    Requirement: The AI Summarizer engine should accept chart & trend data 
    and return a non-empty HTML string suitable for morning emails.
    """
    from src.summarizer import generate_morning_brief

    mock_chart_data = {
        "symbol": "BTC/USD",
        "price": 67450.00,
        "summary": "Higher highs forming on 4h timeframe."
    }
    mock_trends = [
        {"platform": "TikTok", "topic": "#AIAutomation", "volume": "12.4M views"}
    ]

    with patch("src.summarizer.genai.Client") as mock_client_class:
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.text = "<h1>Morning Executive Briefing</h1><p>Market is bullish.</p>"
        mock_client.models.generate_content.return_value = mock_response
        mock_client_class.return_value = mock_client

        report = generate_morning_brief(mock_chart_data, mock_trends, api_key="test-key")

        assert isinstance(report, str), "Report should be a string"
        assert len(report) > 0, "Report should not be empty"
        assert "Morning Executive Briefing" in report