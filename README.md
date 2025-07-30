# Jira Worklog Automation using Google Sheets

Automate posting worklogs to Jira from a structured Google Sheet using Python and the Google Sheets API.

## ✅ Prerequisites
- Python3 should be installed in the machine
- Jira account Personal Access Token (PAT)
- Google account with access to the target Google Sheet
- Should be connected to JTG's VPN (I outside office)

## Clone this repository to local machine
```
git clone https://github.com/vinay7330/Automate_worklogs_from_sheets_to_jira.git
```
---

## 🔧 Step 1: Google Cloud Setup for Sheets API

### 1.1 Enable Sheets API

- Go to [Google Cloud Console](https://console.cloud.google.com/)
- Create a new project or use an existing one
- Navigate to **APIs & Services > Library**
- Search and enable **Google Sheets API**

### 1.2 Configure OAuth Consent Screen

- Go to **APIs & Services > OAuth consent screen**
- Choose **External** (or Internal for Google Workspace)
- Fill required app details and save
- You may skip scopes and test users for personal use

### 1.3 Create OAuth Credentials

- Go to **Credentials > Create Credentials > OAuth client ID**
- Select **Desktop App**
- Name it (e.g., `Jira Worklog Automation`)
- Download the generated `credentials.json`
- Save it in your project root folder

---

## 🔐 Step 2: Generate Jira Personal Access Token (PAT)

- Log in to your Jira account
- Click your profile > **Personal Access Tokens**
- Click **Create token**
- Add a descriptive name and optional expiry
- Copy and save the PAT securely

---

## 📁 Step 3: Project Setup & Dependencies

### 3.1 Project Structure
```
project-root/
├─ credentials.json # Google OAuth credentials
├─ .env # Store secrets 
├─ main.py # Main script
└─ README.md # This file
```
### 3.2 Create `.env` File

Create a file named `.env` in the root directory:

```
JIRA_PAT = your_jira_personal_access_token_here
SPREADSHEET_ID = your_google_sheet_id_here   // Will be found in your sheet's URL
JIRA_DOMAIN =  your_jira_domain // like "jira.jtg.tools"
```

### 3.3 Create and Activate Virtual Environment 
# Create a virtual environment
```
python3 -m venv venv
```

# Activate on Linux/macOS
```
source venv/bin/activate
```

# Activate on Windows
```
venv\Scripts\activate
```

### 3.4 Install Dependencies
```
pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client requests python-dotenv
```
### 3.5 Cross Verification before running script 

<img width="423" height="71" alt="image" src="https://github.com/user-attachments/assets/e4f63409-8c86-4d82-aef1-07a094167d96" />

```
| Parameter      | Description                                                                                                    |   Example     |
| -------------- | ---------------------------------------------------------------------------------------------------------------| ------------- |
| `tab_name`     | The "name of the sheet/tab" in the Google Sheet that contains your timesheet data                              | `"July 2025"` |
| `start_column` | The "starting column letter" in the timesheet from where worklog entries should be added (shown in above img)  |     "A"       |
| `end_column`   | The "ending column letter" in the timesheet until where worklog entries should be added                        |     "AE"      |
```
### 🛡️ Note: This script is idempotent. This means you can run it multiple times without risk of duplicate entries. It will:
- Skip already-added worklogs
- Add only new or previously-missing entries ( So need not to worry 😉 )
  
### 3.6 Run the script & Authorize the application
```
python3 main.py 
```
