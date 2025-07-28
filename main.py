from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import requests
from datetime import datetime, timezone, timedelta
from dotenv import load_dotenv
import os

load_dotenv()
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
JIRA_PAT = os.getenv("JIRA_PAT")
AUTH_TOKEN =os.getenv("AUTH_TOKEN")
JIRA_API_URL = f"https://{os.getenv("JIRA_DOMAIN")}/rest/api/2/issue/{{issue_key}}/worklog"

def convert_to_hours(time_list):
    total = 0.0
    for val in time_list:
        try:
            total += float(val)
        except Exception:
            pass
    return total

def format_started_datetime():
    IST = timezone(timedelta(hours=5, minutes=30))  
    now = datetime.now(IST)
    return now.strftime('%Y-%m-%dT%H:%M:%S.000%z')

def format_time_spent(hours):
    h = int(hours)
    m = int(round((hours - h)*60))
    if h > 0 and m > 0:
        return f"{h}h {m}m"
    elif h > 0:
        return f"{h}h"
    else:
        return f"{m}m"


def post_worklog(issue_key, started, time_spent, comment):
    url = JIRA_API_URL.format(issue_key=issue_key)
    headers = {
        "Authorization": f"Bearer {JIRA_PAT}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    payload = {
        "comment": comment,
        "started": started,
        "timeSpent": time_spent
    }
    resp = requests.post(url, json=payload, headers=headers)
    return resp


def has_time_in_columns(row, start, end):
    for i in range(start, end + 1):
        if len(row) > i and row[i].strip() != "":
            try:
                if float(row[i]) > 0:
                    return True
            except Exception:
                pass
    return False

def col_letter_to_index(col_letter):
    col = col_letter.upper()
    index = 0
    for c in col:
        index = index * 26 + (ord(c) - ord('A') + 1)
    return index - 1

def main(tab_name, start_col_letter, end_col_letter):
    start_index = col_letter_to_index(start_col_letter)
    end_index = col_letter_to_index(end_col_letter)

    flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
    creds = flow.run_local_server(port=0)
    sheets_service = build('sheets', 'v4', credentials=creds)

    SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")
    RANGE_NAME = f"{tab_name}!A7:{end_col_letter}" 

    print(f"Fetching data from range: {RANGE_NAME}")

    try:
        result = sheets_service.spreadsheets().values().get(
            spreadsheetId=SPREADSHEET_ID,
            range=RANGE_NAME
        ).execute()
    except Exception as e:
        print(f"Failed to fetch spreadsheet data: {e}")
        return

    values = result.get('values', [])
    if not values:
        print("No data found.")
        return

    for idx, row in enumerate(values, start=7):
        if not has_time_in_columns(row, start_index, end_index):
            continue

        issue_key = row[5]  
        comment = row[8] 
        time_cells = row[start_index:end_index + 1] 
        total_hours = convert_to_hours(time_cells)

        if total_hours == 0:
            continue

        started_dt = format_started_datetime()
        time_spent_str = format_time_spent(total_hours)

        print(f"Row {idx}: Worklog for {issue_key} - {time_spent_str} started at {started_dt}")

        response = post_worklog(issue_key, started_dt, time_spent_str, comment)
        if response.status_code == 201:
            print(f"Row {idx}: Worklog added successfully.")
        else:
            print(f"Row {idx}: Failed to add worklog - Status {response.status_code}, Response: {response.text}")

if __name__ == "__main__":
    main("July 2025","AAA", "AAAA")
