import os
import datetime
import base64
from email.message import EmailMessage

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# --- CONFIGURATION ---
# To change the recipient, subject, or body of the email, update these variables:
GMAIL_RECIPIENT = "mailproject329@gmail.com"
GMAIL_SUBJECT = "AI Agent Gmail Test"
GMAIL_BODY = "This is a test draft created by the AI agent using the Gmail API."

# To change the calendar event details, update these variables:
CALENDAR_SUMMARY = "AI Agent Calendar Test"
CALENDAR_DESCRIPTION = "This is a test event created by the AI agent using the Google Calendar API."
EVENT_DURATION_MINUTES = 60
HOURS_FROM_NOW = 4

# File paths
SCOPES = [
    "https://www.googleapis.com/auth/gmail.compose",
    "https://www.googleapis.com/auth/calendar.events",
]
TOKEN_PATH = "token.json"
# We look for the specific client secret file found in the directory
CLIENT_SECRET_FILE = "client_secret_260508869832-arhko3c15sskj6tvfgalbht1pq3vj9eq.apps.googleusercontent.com.json"


def get_credentials():
    """
    Handles OAuth2 authentication and token management.
    Returns valid credentials.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first time.
    if os.path.exists(TOKEN_PATH):
        try:
            creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
        except Exception as e:
            print(f"Error loading {TOKEN_PATH}: {e}")
            creds = None

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                print("Refreshing expired token...")
                creds.refresh(Request())
            except Exception as e:
                print(f"Failed to refresh token: {e}")
                creds = None
        
        if not creds:
            if not os.path.exists(CLIENT_SECRET_FILE):
                # Fallback to generic name
                if os.path.exists("credentials.json"):
                    CLIENT_SECRET_FILE_ACTUAL = "credentials.json"
                else:
                    raise FileNotFoundError(
                        f"CRITICAL ERROR: Google client secret file not found.\n"
                        f"Expected file: {CLIENT_SECRET_FILE} or credentials.json\n"
                        f"Please place the JSON file from Google Cloud Console in this folder."
                    )
            else:
                CLIENT_SECRET_FILE_ACTUAL = CLIENT_SECRET_FILE

            print(f"Starting new authentication flow using {CLIENT_SECRET_FILE_ACTUAL}...")
            try:
                flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE_ACTUAL, SCOPES)
                creds = flow.run_local_server(port=0)
                # Save the credentials for the next run
                with open(TOKEN_PATH, "w") as token:
                    token.write(creds.to_json())
                print(f"Token saved to {TOKEN_PATH}")
            except Exception as e:
                raise RuntimeError(f"Authentication failure: {e}")

    return creds


def create_gmail_draft(creds):
    """
    Creates a draft email in Gmail.
    """
    try:
        service = build("gmail", "v1", credentials=creds)
        
        message = EmailMessage()
        message.set_content(GMAIL_BODY)
        message["To"] = GMAIL_RECIPIENT
        message["From"] = "me"
        message["Subject"] = GMAIL_SUBJECT

        # Encoded message
        encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

        create_draft_body = {"message": {"raw": encoded_message}}

        draft = service.users().drafts().create(userId="me", body=create_draft_body).execute()

        print(f"SUCCESS: Gmail draft created. Draft ID: {draft['id']}")
        return draft

    except HttpError as error:
        print(f"ERROR: A Gmail API error occurred: {error}")
        return None
    except Exception as e:
        print(f"ERROR: An unexpected error occurred during Gmail draft creation: {e}")
        return None


def create_calendar_event(creds):
    """
    Creates a Google Calendar event.
    """
    try:
        service = build("calendar", "v3", credentials=creds)

        # Time calculation
        now = datetime.datetime.now(datetime.timezone.utc)
        start_time = now + datetime.timedelta(hours=HOURS_FROM_NOW)
        end_time = start_time + datetime.timedelta(minutes=EVENT_DURATION_MINUTES)

        # Format times as ISO 8601 strings
        start_iso = start_time.isoformat()
        end_iso = end_time.isoformat()

        event = {
            "summary": CALENDAR_SUMMARY,
            "description": CALENDAR_DESCRIPTION,
            "start": {
                "dateTime": start_iso,
                "timeZone": "UTC",
            },
            "end": {
                "dateTime": end_iso,
                "timeZone": "UTC",
            },
        }

        event = service.events().insert(calendarId="primary", body=event).execute()
        
        print(f"SUCCESS: Calendar event created: {event.get('htmlLink')}")
        print(f"Event Time: {start_time.strftime('%Y-%m-%d %H:%M:%S UTC')} (Duration: {EVENT_DURATION_MINUTES} mins)")
        return event

    except HttpError as error:
        print(f"ERROR: A Calendar API error occurred: {error}")
        return None
    except Exception as e:
        print(f"ERROR: An unexpected error occurred during Calendar event creation: {e}")
        return None


def main():
    print("--- AI Agent Google API Test Program ---")
    try:
        # Step 1: Authenticate
        creds = get_credentials()

        # Step 2: Create Gmail Draft
        print("\n[Action 1] Creating Gmail Draft...")
        create_gmail_draft(creds)

        # Step 3: Create Calendar Event
        print("\n[Action 2] Creating Calendar Event...")
        create_calendar_event(creds)

    except FileNotFoundError as e:
        print(f"\nSETUP ERROR: {e}")
    except RuntimeError as e:
        print(f"\nAUTH ERROR: {e}")
    except Exception as e:
        print(f"\nCRITICAL ERROR: {e}")


if __name__ == "__main__":
    main()
