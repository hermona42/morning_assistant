import os
import logging
from google import genai

logger = logging.getLogger("src.summarizer")

def generate_morning_brief(
    chart_data: dict, 
    trends_data: list, 
    sentiment_data: dict = None, 
    api_key: str = None
) -> str:
    """
    Takes raw chart, social trend, and sentiment data, formats it into a prompt,
    and calls Google Gemini to generate an executive HTML briefing.
    """
    api_key = api_key or os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable is missing.")

    sentiment = sentiment_data or {"score": "50", "classification": "Neutral"}
    client = genai.Client(api_key=api_key)

    formatted_trends = []
    for t in trends_data:
        if isinstance(t, dict):
            formatted_trends.append(f"{t.get('platform', 'Trend')}: {t.get('topic', '')} ({t.get('volume', '')})")
        else:
            formatted_trends.append(str(t))

    prompt = f"""
    You are an executive assistant preparing a daily morning briefing.
    
    Data Provided:
    1. Market Chart: Symbol {chart_data.get('symbol')}, Price {chart_data.get('price')}, Summary: {chart_data.get('summary')}
    2. Viral Social Trends: {', '.join(formatted_trends)}
    3. Market Sentiment Index: {sentiment.get('score')}/100 ({sentiment.get('classification')})
    
    Include a top-level visual badge displaying the overall Market Sentiment classification.
    Please generate a sleek, professional, single-page HTML email body. 
    Use inline CSS for styling. Include an executive overview, chart highlights, and key trend takeaways.
    Return ONLY valid HTML code inside <div> tags without markdown backticks.
    """

    try:
        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt,
        )
        return response.text
    except Exception as e:
        logger.error(f"Error generating AI brief: {e}")
        return f"<p>Error calling AI engine: {e}</p>"