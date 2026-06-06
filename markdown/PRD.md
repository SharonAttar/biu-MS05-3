\# Product Requirement Document (PRD) - Gmail-to-Calendar AI Agent



\## 1. Introduction \& Objectives

In the modern digital workspace, scheduling and calendar management are primarily driven by daily email communications. Manual coordination requires reading emails, extracting details, checking calendar availability, and manually entering events—a time-consuming process prone to human error.

The objective of this project is to develop an autonomous AI Agent that integrates Large Language Model (LLM) capabilities with Google APIs (Gmail and Google Calendar). The system will automatically identify meeting requests in natural language, extract relevant event details, and intelligently manage the user's schedule.



\## 2. Stakeholders \& Target Users

\* \*\*Professionals and Students:\*\* End-users looking to automate their personal calendar management directly from their email inbox.

\* \*\*Academic Evaluation Team (Dr. Yoram Segal):\*\* Reviewing the implementation of agent architecture, rigid API consumption, LLM-based natural language translation, and adherence to security best practices.



\## 3. System Architecture \& Component Levels

As defined in the course lectures, the system is built hierarchically:

1\. \*\*Software / API Layer:\*\* Direct, rigid connection to Google APIs (Gmail and Calendar) requiring parameters in a precise, fixed format.

2\. \*\*Skill Layer:\*\* Functions wrapping the API code, allowing them to be triggered via natural language understanding (e.g., "extract meeting details", "check availability").

3\. \*\*Agent Layer:\*\* The central orchestrator that runs iteratively, manages the Context Window (CW), dynamically selects the appropriate skills, and handles edge cases autonomously.



\## 4. Functional Requirements

\* \*\*FR-1: Smart Inbox Scanning:\*\* The agent shall scan unread emails using a targeted search query (e.g., limited timeframe or custom category filtering).

\* \*\*FR-2: Email Intent Classification:\*\* The system must reliably differentiate between an email containing a meeting request and a general information email.

\* \*\*FR-3: Natural Language Information Extraction:\*\* An LLM shall parse free-text emails (supporting Hebrew and English) to extract critical event entities: Subject, Date, Time, Attendees, and Location/Link.

\* \*\*FR-4: Conflict Detection:\*\* Prior to booking, the agent shall query the Google Calendar API to verify if the requested time slot is available.

\* \*\*FR-5: Automated Event Creation:\*\* If the time slot is free, the agent shall automatically create a calendar event containing the meeting description and a reference link back to the source email.

\* \*\*FR-6: Smart Replies \& Edge Cases:\*\*

&#x20; \* \*\*Time Slot Conflicted:\*\* The system shall reply to the sender stating that the meeting cannot be scheduled at the requested time.

&#x20; \* \*\*Missing Mandatory Info:\*\* If critical details (like date or time) are missing, the agent shall create a Gmail Draft requesting clarification from the sender.

\* \*\*FR-7: Duplicate Prevention:\*\* To avoid redundant processing, successfully handled emails shall be labeled with an `AI\_PROCESSED` tag.



\## 5. Non-Functional Requirements

\* \*\*NFR-1: Data Security:\*\* \* Strict prohibition against committing or uploading sensitive credentials (`API Key`, `Client ID`, `Token`) to GitHub repositories.

&#x20; \* Utilization of a `.gitignore` file to safeguard local authentication structures (`client\_secret.json`, `token.json`).

&#x20; \* Configuration and credential parameters must be handled via environment variables.

\* \*\*NFR-2: Safe Mode (Dry Run):\*\* The codebase must support a `DRY\_RUN` flag to simulate full agent workflows and logging without committing active state changes to the live Google APIs.

\* \*\*NFR-3: Modern Package Management:\*\* Environment and dependency management must be isolated and maintained using the `uv` toolchain (`pyproject.toml` and `uv.lock`).

