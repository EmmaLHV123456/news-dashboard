# Frontier Tech News Aggregator

A minimal news aggregator for VC managers focused on crypto (70%) and AI (30%).

## Features

- **RSS Collection**: Pulls from The Block, CoinDesk, TechCrunch, VentureBeat, SEC
- **DefiLlama Integration**: Free API for crypto funding rounds
- **Auto-categorization**: Tags articles as funding, regulatory, crypto, AI
- **Google Sheets**: Live spreadsheet with all articles
- **Email Digest**: Daily summary of top news

## Quick Start

```bash
# Install dependencies
cd ~/projects/news-aggregator
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Test run (no outputs, just collects)
python main.py --dry-run
```

## Setup Google Sheets

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project
3. Enable "Google Sheets API"
4. Create OAuth 2.0 credentials (Desktop app)
5. Download `credentials.json` to this directory
6. Create a new Google Sheet and copy the ID from the URL
7. Add to `.env`:
   ```
   GOOGLE_SHEETS_CREDENTIALS_FILE=credentials.json
   SPREADSHEET_ID=your_sheet_id_here
   ```

First run will open a browser for Google auth.

## Setup Email

For Gmail, you need an App Password:

1. Enable 2FA on your Google account
2. Go to [App Passwords](https://myaccount.google.com/apppasswords)
3. Generate a password for "Mail"
4. Add to `.env`:
   ```
   EMAIL_SENDER=your_email@gmail.com
   EMAIL_PASSWORD=your_app_password
   EMAIL_RECIPIENTS=you@example.com
   ```

## Usage

```bash
# Full run (Sheets + Email)
python main.py

# Just collect, preview in terminal
python main.py --dry-run

# Skip email
python main.py --no-email

# Last 48 hours of news
python main.py --hours 48

# Last 14 days of funding rounds
python main.py --raises-days 14
```

## Schedule Daily Run

Add to crontab (`crontab -e`):

```cron
# Run at 7am daily
0 7 * * * cd ~/projects/news-aggregator && ./venv/bin/python main.py >> cron.log 2>&1
```

## Customize Sources

Edit `config.py` to:
- Add/remove RSS feeds
- Adjust keyword filters
- Change category definitions

## Project Structure

```
news-aggregator/
├── main.py              # Entry point
├── config.py            # Sources & keywords
├── collectors/
│   ├── rss_collector.py     # RSS feed parser
│   └── defillama_collector.py  # Crypto funding data
├── outputs/
│   ├── google_sheets.py     # Sheets integration
│   └── email_digest.py      # Email sender
└── requirements.txt
```
