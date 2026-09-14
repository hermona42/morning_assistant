import pytest

def test_fetch_chart_data_returns_dict():
    """
    Requirement: Chart Fetcher must return market chart info as a dictionary.
    Keys expected: 'symbol', 'price', and 'summary'.
    """
    from src.fetchers import fetch_chart_data

    result = fetch_chart_data("BTC/USD")
    
    # Assertions check if our expectations are met
    assert isinstance(result, dict), "Output should be a dictionary"
    assert "symbol" in result, "Missing 'symbol' key"
    assert "price" in result, "Missing 'price' key"


def test_fetch_trends_returns_list():
    """
    Requirement: Social Trend Fetcher must return a list of top trending topics.
    """
    from src.fetchers import fetch_social_trends

    trends = fetch_social_trends()
    
    assert isinstance(trends, list), "Output should be a list"
    assert len(trends) > 0, "Trend list should not be empty"