\# TODO List - Gmail-to-Calendar AI Agent Project



\## Security \& Infrastructure 🛠️

\- \[x] Establish a local Python 3.13+ runtime environment managed via `uv`.

\- \[x] Configure `.gitignore` to exclude `client\_secret\_\*.json`, `token.json`, and run logs.

\- \[x] Provision a Google Cloud Console project and enable Gmail and Google Calendar APIs.

\- \[ ] Migrate raw authentication configs and hardcoded scripts to secure system Environment Variables.



\## Email Scanning, Filtering \& Classification 📧

\- \[x] Authenticate with Gmail API and implement fetching loops for unread messages.

\- \[x] Implement a structural `MEETING\_KEYWORDS` array for initial bilingual keyword filtering.

\- \[ ] Embed a dedicated LLM prompt to guarantee precise classification between at least 2 distinct email types (Meeting invite vs. General mail).

\- \[x] Implement duplicate execution guards utilizing the `AI\_PROCESSED` label workflow.



\## Data Extraction \& Calendar Integration 📅

\- \[x] Script LLM entity extraction logic to parse unstructured dates, times, and attendees from raw body text.

\- \[ ] Develop conflict-checking logic utilizing the Google Calendar free/busy API endpoints.

\- \[x] Script standard calendar event insertion functions for successful matches.



\## Automated Exception Handling \& Smart Response 🤖

\- \[ ] Integrate conflict routing to trigger automated rejection/reschedule emails when a time slot is taken.

\- \[x] Code missing-information workflows to automatically generate a clear Gmail Draft requesting detail completions.

\- \[x] Validate and expose the structural `DRY\_RUN` flag logic across main modules.



\## Testing, Documentation \& Submission 📑

\- \[x] Author a fast PowerShell execution script (`run\_agent.ps1`) bypassing default execution scopes cleanly.

\- \[ ] Execute comprehensive End-to-End (E2E) validations inside a dedicated test Gmail account.

\- \[ ] Consolidate engineering artifacts (`PRD`, `TODO`, `PLAN`) into a shared `docs/` folder, synchronize the team GitHub repository, and submit to the lecturer.

