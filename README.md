# Gmail-to-Calendar AI Agent

A smart Python agent that monitors your Gmail inbox for meeting requests and automatically schedules them in Google Calendar.

## Features
- **Automated Monitoring**: Scans unread emails for meeting-related keywords.
- **Intelligent Extraction**: Uses natural language parsing to identify dates and times for meetings.
- **Automatic Scheduling**: Creates Google Calendar events with descriptions and links back to the source email.
- **Smart Replies**: If a meeting intent is detected but the date/time is missing, it creates a Gmail draft reply asking for details.
- **Duplicate Prevention**: Marks processed emails with an `AI_PROCESSED` label to ensure they aren't handled twice.
- **Safe Mode**: Includes a `DRY_RUN` setting for testing without making actual changes.

## Prerequisites
- **Python 3.13+**
- **uv**: A fast Python package and project manager.
- **Google Cloud Project**: With Gmail and Google Calendar APIs enabled.

## Setup

### 1. Project Files
Ensure you have the following files in your project directory:
- `client_secret_*.json`: Your Google OAuth2 credentials from the Google Cloud Console.
- `gmail_calendar_agent.py`: The main agent script.
- `run_agent.ps1`: A PowerShell runner script for easy execution.

### 2. Dependencies
Install the required libraries using `uv`:
```bash
uv add google-api-python-client google-auth-httplib2 google-auth-oauthlib python-dateutil
```

## How to Run

### Manual Run
Run the agent directly using `uv`:
```powershell
uv run python gmail_calendar_agent.py
```

### Using the PowerShell Runner
For a more convenient execution with logging:
```powershell
powershell.exe -ExecutionPolicy Bypass -File .\run_agent.ps1
```

## Configuration
Open `gmail_calendar_agent.py` to modify settings:
- `DRY_RUN`: Set to `True` for testing, `False` for live operation.
- `LABEL_NAME`: The Gmail label used to mark processed emails (default: `AI_PROCESSED`).
- `MEETING_KEYWORDS`: A list of words (English and Hebrew) used to detect meeting requests.

## Files and Logs
- `token.json`: Generated after the first login; stores your authentication.
- `agent_run.log`: Contains the history of all agent activities and errors.

## Troubleshooting
- **Insufficient Permissions**: Delete `token.json` and run the script again to re-authenticate with the required scopes.
- **API Errors**: Ensure both the Gmail API and Google Calendar API are enabled in your Google Cloud Console.
