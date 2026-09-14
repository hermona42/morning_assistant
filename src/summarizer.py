import logging
import os
from typing import Dict, List, Any
from google import genai

logger = logging.getLogger(__name__)


def generate_morning_brief(chart_data: Dict[str, Any], trend_data: List[Dict[str, Any]], api_key: str = None) -> str:
    """
    Generates an executive morning report using Google Gemini API.
    
    Args:
        chart_data (dict): Market chart telemetry.
        trend_data (list): Social and news trend listings.
        api_key (str, optional): Gemini API key. Defaults to GEMINI_API_KEY environment variable.
        
    Returns:
        str: HTML formatted morning report.
    """
    resolved_key = api_key or os.getenv("GEMINI_API_KEY")
    
    if not resolved_key:
        logger.warning("No GEMINI_API_KEY provided. Returning fallback report.")
        return f"<h2>Daily Briefing (Fallback)</h2><p>Market: {chart_data.get('summary', 'N/A')}</p>"

    try:
        client = genai.Client(api_key=resolved_key)
        
        prompt = f"""
        You are an executive morning briefing AI agent. 
        Synthesize the following telemetry into a crisp, readable HTML email digest.
        
        --- FINANCIAL CHART DATA ---
        Symbol: {chart_data.get('symbol')}
        Price: {chart_data.get('price')} {chart_data.get('currency', 'USD')}
        Summary: {chart_data.get('summary')}
        
        --- VIRAL TREND DATA ---
        {trend_data}
        
        Provide the response formatted in modern, clean HTML with styled section headers.
        """
        
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )
        return response.text

    except Exception as e:
        logger.error(f"Error generating AI brief: {e}")
        return f"<h2>Daily Briefing</h2><p>Error calling AI engine: {e}</p>"