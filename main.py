import os
import logging
from dotenv import load_dotenv

from src.fetchers import fetch_chart_data, fetch_social_trends, fetch_sentiment_index
from src.summarizer import generate_morning_brief
from src.notifier import send_email_report

# Configure logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("MorningAssistant")

def main():
    # Load environment variables from .env file
    load_dotenv()
    
    logger.info("=== Starting Morning Assistant AI Agent Pipeline ===")

    # 1. Fetch Market Chart Data
    logger.info("Fetching market chart data...")
    chart_data = fetch_chart_data(symbol="bitcoin")

    # 2. Fetch Viral Trends Data
    logger.info("Fetching viral trends data...")
    trends_data = fetch_social_trends()

    # 3. Fetch Market Sentiment Index
    logger.info("Fetching market sentiment index...")
    sentiment_data = fetch_sentiment_index()

    # 4. Generate AI Morning Briefing via Gemini 3.6-flash
    logger.info("Generating AI summary via Gemini 3.6 Flash...")
    try:
        html_brief = generate_morning_brief(
            chart_data=chart_data,
            trends_data=trends_data,
            sentiment_data=sentiment_data
        )
    except Exception as e:
        logger.error(f"Failed to generate AI brief: {e}")
        return

    # 5. Dispatch Email Report via SMTP
    sender_email = os.getenv("SENDER_EMAIL")
    sender_password = os.getenv("SENDER_PASSWORD")
    recipient_email = os.getenv("RECIPIENT_EMAIL")

    if not all([sender_email, sender_password, recipient_email]):
        logger.error("Missing email configuration environment variables.")
        return

    logger.info(f"Sending daily email report to {recipient_email}...")
    success = send_email_report(
        subject="🌅 Executive Morning Briefing",
        body_html=html_brief,
        recipient_email=recipient_email,
        sender_email=sender_email,
        sender_password=sender_password
    )

    if success:
        logger.info("🎉 Morning Briefing delivered successfully!")
    else:
        logger.error("❌ Failed to deliver Morning Briefing email.")

if __name__ == "__main__":
    main()