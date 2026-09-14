from unittest.mock import patch, MagicMock
from src.notifier import send_email_report

def test_send_email_report_success():
    """
    Requirement: Email notifier must build a valid MIME message and send it via SMTP.
    """
    with patch("smtplib.SMTP") as mock_smtp:
        mock_instance = MagicMock()
        mock_smtp.return_value.__enter__.return_value = mock_instance
        
        success = send_email_report(
            subject="Test Morning Digest",
            body_html="<h1>Good morning!</h1>",
            recipient_email="test@example.com",
            sender_email="sender@example.com",
            sender_password="secretpassword"
        )
        
        assert success is True
        assert mock_instance.starttls.called
        assert mock_instance.login.called
        assert mock_instance.send_message.called