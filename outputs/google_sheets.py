"""
Google Sheets output - push aggregated news to a spreadsheet
"""
import os
from datetime import datetime
from typing import List, Dict
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import pickle

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]


def get_sheets_service():
    """Authenticate and return Google Sheets service"""
    creds = None
    token_path = "token.pickle"
    creds_file = os.getenv("GOOGLE_SHEETS_CREDENTIALS_FILE", "credentials.json")

    if os.path.exists(token_path):
        with open(token_path, "rb") as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(creds_file, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(token_path, "wb") as token:
            pickle.dump(creds, token)

    return build("sheets", "v4", credentials=creds)


def push_articles_to_sheet(articles: List[Dict], spreadsheet_id: str, sheet_name: str = "News"):
    """Push articles to Google Sheet"""
    service = get_sheets_service()

    # Prepare header row
    headers = ["Date", "Source", "Title", "Categories", "Funding?", "Regulatory?", "Link"]

    # Prepare data rows
    rows = [headers]
    for article in articles:
        rows.append([
            article["published"][:10],  # Just the date
            article["source"],
            article["title"],
            ", ".join(article.get("categories", [])),
            "YES" if article.get("is_funding") else "",
            "YES" if article.get("is_regulatory") else "",
            article["link"],
        ])

    # Clear existing data and write new
    range_name = f"{sheet_name}!A:G"
    service.spreadsheets().values().clear(
        spreadsheetId=spreadsheet_id,
        range=range_name
    ).execute()

    service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id,
        range=f"{sheet_name}!A1",
        valueInputOption="RAW",
        body={"values": rows}
    ).execute()

    print(f"Pushed {len(articles)} articles to Google Sheet")


def push_raises_to_sheet(raises: List[Dict], spreadsheet_id: str, sheet_name: str = "Funding Rounds"):
    """Push funding rounds to Google Sheet"""
    service = get_sheets_service()

    headers = ["Date", "Project", "Amount", "Round", "Category", "Lead Investors", "Chains"]

    rows = [headers]
    for r in raises:
        rows.append([
            r["date"][:10],
            r["project"],
            r["amount"],
            r["round"],
            r["category"],
            ", ".join(r.get("lead_investors", [])[:3]),
            ", ".join(r.get("chains", [])),
        ])

    range_name = f"{sheet_name}!A:G"
    service.spreadsheets().values().clear(
        spreadsheetId=spreadsheet_id,
        range=range_name
    ).execute()

    service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id,
        range=f"{sheet_name}!A1",
        valueInputOption="RAW",
        body={"values": rows}
    ).execute()

    print(f"Pushed {len(raises)} funding rounds to Google Sheet")
