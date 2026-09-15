import logging
import requests
import xml.etree.ElementTree as ET

logger = logging.getLogger("src.fetchers")

def fetch_chart_data(symbol: str = "bitcoin") -> dict:
    """
    Fetches live market chart price and 24h stats from CoinGecko API.
    """
    url = f"https://api.coingecko.com/api/v3/simple/price"
    params = {
        "ids": symbol.lower(),
        "vs_currencies": "usd",
        "include_24hr_change": "true",
        "include_24hr_vol": "true"
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        coin_data = data.get(symbol.lower(), {})
        price = coin_data.get("usd", 0.0)
        change_24h = coin_data.get("usd_24h_change", 0.0)
        
        return {
            "symbol": symbol.upper(),
            "price": round(price, 2),
            "summary": f"24h Price Change: {change_24h:+.2f}%"
        }
    except Exception as e:
        logger.error(f"Error fetching live chart data: {e}")
        # Graceful fallback
        return {
            "symbol": symbol.upper(),
            "price": 0.0,
            "summary": "Live data temporarily unavailable"
        }

def fetch_social_trends() -> list:
    """
    Fetches real-time viral search trends via Google Trends RSS feed.
    """
    rss_url = "https://trends.google.com/trending/rss?geo=US"
    
    try:
        response = requests.get(rss_url, timeout=10)
        response.raise_for_status()
        
        root = ET.fromstring(response.content)
        trends = []
        
        # Parse top 5 trending search items from RSS
        for item in root.findall(".//item")[:5]:
            title = item.find("title").text if item.find("title") is not None else "Unknown"
            traffic = item.find("{https://trends.google.com/trending/rss}approx_traffic")
            traffic_text = traffic.text if traffic is not None else "Surging"
            
            trends.append({
                "platform": "Google Trends",
                "topic": title,
                "volume": traffic_text
            })
            
        return trends if trends else [{"platform": "Trends", "topic": "AI & Tech Markets", "volume": "High"}]
    except Exception as e:
        logger.error(f"Error fetching live social trends: {e}")
        return [{"platform": "Trends", "topic": "General Tech Trends", "volume": "N/A"}]