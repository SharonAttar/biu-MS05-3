import os
import datetime
import base64
import re
import json
from email.message import EmailMessage
from dateutil import parser as date_parser

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# --- CONFIGURATION ---
# Set DRY_RUN to True to only print what the agent WOULD do without making changes.
DRY_RUN = False

LABEL_NAME = "AI_PROCESSED"
SCOPES = [
    "https://www.googleapis.com/auth/gmail.modify",   # To read and label emails
    "https://www.googleapis.com/auth/gmail.compose",  # To create draft replies
    "https://www.googleapis.com/auth/calendar.events",# To create calendar events
]

TOKEN_PATH = "token.json"
CLIENT_SECRET_FILE = "client_secret_260508869832-arhko3c15sskj6tvfgalbht1pq3vj9eq.apps.googleusercontent.com.json"

# Keywords that suggest a meeting request
MEETING_KEYWORDS = [
    "meeting", "schedule", "appointment", "call", "zoom", "meet",
    "ניפגש", "פגישה", "שיחה", "לקבוע", "לוז", "מחר", "היום"
]

def get_credentials():
    creds = None
    if os.path.exists(TOKEN_PATH):
        try:
            creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
        except Exception as e:
            print(f"DEBUG: Error loading token: {e}")
            creds = None

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print("Refreshing token...")
            creds.refresh(Request())
        else:
            print("Starting new authentication flow...")
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
            creds = flow.run_local_server(port=0)

        with open(TOKEN_PATH, "w") as token:
            token.write(creds.to_json())
    return creds

def get_gmail_service(creds):
    return build("gmail", "v1", credentials=creds)

def get_calendar_service(creds):
    return build("calendar", "v3", credentials=creds)

def ensure_label_exists(service):
    """Ensures the AI_PROCESSED label exists in Gmail."""
    try:
        results = service.users().labels().list(userId="me").execute()
        labels = results.get("labels", [])
        for label in labels:
            if label["name"] == LABEL_NAME:
                return label["id"]

        # Create label if not found
        print(f"Creating label: {LABEL_NAME}")
        label_obj = {
            "name": LABEL_NAME,
            "labelListVisibility": "labelShow",
            "messageListVisibility": "show"
        }
        created_label = service.users().labels().create(userId="me", body=label_obj).execute()
        return created_label["id"]
    except Exception as e:
        print(f"Error ensuring label exists: {e}")
        return None

def analyze_email_content(subject, body):
    """
    Analyzes email for meeting intent and extracts date/time.
    Returns: (is_meeting, extracted_date, missing_info)
    """
    full_text = f"{subject} {body}".lower()
    is_meeting = any(keyword in full_text for keyword in MEETING_KEYWORDS)

    if not is_meeting:
        return False, None, None

    # Try to extract a date
    try:
        # We look for date-like strings. Fuzzy=True allows parsing dates within text.
        extracted_date = date_parser.parse(full_text, fuzzy=True, ignoretz=True)

        # If the extracted date is in the past (e.g. user said '5pm' and it's 6pm),
        # assume they mean tomorrow.
        if extracted_date < datetime.datetime.now():
             extracted_date = extracted_date + datetime.timedelta(days=1)

        return True, extracted_date, None
    except:
        # If parsing fails, we have a meeting intent but no clear date
        return True, None, "date/time"

def create_draft_reply(service, thread_id, to_email, original_subject):
    """Creates a draft asking for missing info."""
    message = EmailMessage()
    message.set_content(
        f"Hi,\n\nI received your request regarding '{original_subject}'. "
        "Could you please clarify the preferred date and time for our meeting?\n\n"
        "Best regards,\nAI Assistant"
    )
    message["To"] = to_email
    message["Subject"] = f"Re: {original_subject}"
    message["In-Reply-To"] = thread_id
    message["References"] = thread_id

    encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
    body = {"message": {"raw": encoded_message, "threadId": thread_id}}

    if DRY_RUN:
        print(f"[DRY RUN] Would create draft reply to {to_email}")
    else:
        service.users().drafts().create(userId="me", body=body).execute()
        print(f"SUCCESS: Created draft reply for {to_email}")

def create_calendar_event(service, start_time, summary, description):
    """Creates a 1-hour event in Google Calendar."""
    end_time = start_time + datetime.timedelta(hours=1)

    event = {
        "summary": f"Meeting: {summary}",
        "description": description,
        "start": {"dateTime": start_time.isoformat(), "timeZone": "UTC"},
        "end": {"dateTime": end_time.isoformat(), "timeZone": "UTC"},
    }

    if DRY_RUN:
        print(f"[DRY RUN] Would create Calendar event: '{summary}' at {start_time}")
    else:
        event = service.events().insert(calendarId="primary", body=event).execute()
        print(f"SUCCESS: Created Calendar event: {event.get('htmlLink')}")

def process_messages(gmail, calendar, label_id):
    """Main loop to process unread messages."""
    try:
        # Search for unread messages that haven't been processed by us
        query = f"is:unread -label:{LABEL_NAME}"
        results = gmail.users().messages().list(userId="me", q=query).execute()
        messages = results.get("messages", [])

        if not messages:
            print("No new unread messages to process.")
            return

        print(f"Found {len(messages)} new message(s).")

        for msg in messages:
            msg_data = gmail.users().messages().get(userId="me", id=msg["id"]).execute()
            headers = msg_data["payload"]["headers"]

            subject = next((h["value"] for h in headers if h["name"] == "Subject"), "No Subject")
            sender = next((h["value"] for h in headers if h["name"] == "From"), "Unknown")

            # Extract body
            parts = msg_data["payload"].get("parts", [])
            body = ""
            if not parts:
                body = msg_data["payload"].get("body", {}).get("data", "")
            else:
                for part in parts:
                    if part["mimeType"] == "text/plain":
                        body = part["body"].get("data", "")
                        break

            if body:
                body = base64.urlsafe_b64decode(body).decode()

            print(f"\nAnalyzing message from {sender}: '{subject}'")

            is_meeting, event_date, missing_info = analyze_email_content(subject, body)

            if is_meeting:
                if event_date:
                    print(f"  -> Meeting detected for {event_date}")
                    create_calendar_event(calendar, event_date, subject, f"Automated from email by {sender}\n\n{body[:200]}...")
                else:
                    print(f"  -> Meeting detected but missing {missing_info}. Creating draft reply.")
                    create_draft_reply(gmail, msg["threadId"], sender, subject)
            else:
                print("  -> Not a meeting request. Skipping.")

            # Mark as processed by adding the label
            if not DRY_RUN:
                gmail.users().messages().batchModify(
                    userId="me",
                    body={
                        "ids": [msg["id"]],
                        "addLabelIds": [label_id],
                        "removeLabelIds": ["UNREAD"]
                    }
                ).execute()
                print(f"  -> Marked message {msg['id']} as AI_PROCESSED and READ.")
            else:
                print(f"  -> [DRY RUN] Would mark message {msg['id']} as AI_PROCESSED and READ.")

    except Exception as e:
        print(f"Error during message processing: {e}")

def main():
    print("--- Gmail-to-Calendar AI Agent ---")
    if DRY_RUN:
        print("!!! RUNNING IN SAFE TEST MODE (DRY_RUN = True) !!!")
        print("No actual changes will be made to your Gmail or Calendar.")

    try:
        creds = get_credentials()
        gmail = get_gmail_service(creds)
        calendar = get_calendar_service(creds)

        label_id = ensure_label_exists(gmail)
        if not label_id:
            print("Could not verify/create label. Exiting.")
            return

        process_messages(gmail, calendar, label_id)

    except Exception as e:
        print(f"CRITICAL ERROR: {e}")

if __name__ == "__main__":
    main()
