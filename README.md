# 🌅 Morning Assistant AI Agent

An automated morning briefing agent built with Python, Google Gemini AI, and GitHub Actions. It monitors live crypto charts, TikTok hashtag virality, and Google trends, generating an executive HTML morning digest sent straight to your email.

## 🚀 Features

- **Live Market Tracking:** Polls crypto asset prices and 24h stats via CoinGecko.
- **Social Virality Feeds:** Captures trending TikTok topics and Google search spikes.
- **AI Intelligence:** Uses Google Gemini (`gemini-3.6-flash`) to generate structured executive emails.
- **Automated Delivery:** Runs on a daily cron trigger using free GitHub Actions infrastructure.

## 🛠 Local Setup & Running

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/hermona42/morning_assistant](https://github.com/hermona42/morning_assistant.git)
   cd morning_assistant
```

### 2. Set up virtual environment
```bash
python -m venv venv
# On Windows (Git Bash / CMD):
source venv/Scripts/activate
# On macOS / Linux:
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment Configuration
Create a `.env` file in the project root directory based on `.env.example`:

```env
GEMINI_API_KEY=your_gemini_api_key_here
SENDER_EMAIL=your_gmail_address@gmail.com
SENDER_PASSWORD=your_16_character_app_password
RECIPIENT_EMAIL=recipient_email@gmail.com
```

---

## 🧪 Testing

Run the automated test suite using `pytest`:

```bash
pytest
```

---

## 🚀 Execution

To trigger the pipeline manually from your terminal:

```bash
python main.py
```

---

## ⚙ GitHub Actions Setup (Automated Daily Scheduling)

To enable automatic execution every morning at 06:00 AM UTC:

1. Push your code to your GitHub repository.
2. Go to **Settings** > **Secrets and variables** > **Actions** in your GitHub repo.
3. Add the following **Repository Secrets**:

| Secret Name | Value |
|---|---|
| `GEMINI_API_KEY` | Your Google Gemini API Key |
| `SENDER_EMAIL` | Sender Gmail Address |
| `SENDER_PASSWORD` | Google 16-character App Password |
| `RECIPIENT_EMAIL` | Recipient Email Address |

4. Navigating to the **Actions** tab allows you to trigger on-demand test runs using the **Run workflow** button.