"""
Main execution pipeline for Morning Assistant AI Agent.
Coordinates data fetchers, Gemini AI summarizer, and SMTP email dispatch.
"""

import os
import sys
import logging
from datetime import datetime
from dotenv import load_dotenv

# Automatically load key-value pairs from .env file into environment
load_dotenv()

from src.fetchers import fetch_chart_data, fetch_social_trends
from src.summarizer import generate_morning_brief
from src.notifier import send_email_report

# Configure logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("MorningAssistant")


def run_pipeline() -> None:
    """Executes the end-to-end morning briefing workflow."""
    logger.info("=== Starting Morning Assistant AI Agent Pipeline ===")
    
    # 1. Fetch Telemetry
    logger.info("Fetching market chart data...")
    chart_data = fetch_chart_data("BTC/USD")
    
    logger.info("Fetching viral trends data...")
    trend_data = fetch_social_trends()
    
    # 2. Generate AI Brief
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        logger.error("GEMINI_API_KEY is not set. Exiting execution.")
        sys.exit(1)
        
    logger.info("Generating AI summary via Gemini 2.5 Flash...")
    html_report = generate_morning_brief(chart_data, trend_data, api_key=api_key)
    
    # 3. Deliver Email
    sender_email = os.getenv("SENDER_EMAIL")
    sender_password = os.getenv("SENDER_PASSWORD")
    recipient_email = os.getenv("RECIPIENT_EMAIL", sender_email)
    
    if not sender_email or not sender_password:
        logger.warning("Email credentials (SENDER_EMAIL / SENDER_PASSWORD) missing. Printing report to stdout instead.")
        print("\n--- GENERATED REPORT HTML ---\n")
        print(html_report)
        print("\n-----------------------------\n")
        return

    today_str = datetime.now().strftime("%B %d, %Y")
    subject = f"🌅 Executive Morning Briefing - {today_str}"
    
    logger.info(f"Sending daily email report to {recipient_email}...")
    success = send_email_report(
        subject=subject,
        body_html=html_report,
        recipient_email=recipient_email,
        sender_email=sender_email,
        sender_password=sender_password
    )
    
    if success:
        logger.info("🎉 Morning Briefing delivered successfully!")
    else:
        logger.error("Failed to send morning briefing email.")


if __name__ == "__main__":
    run_pipeline()