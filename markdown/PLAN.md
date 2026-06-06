\# Project Work Plan - Gmail-to-Calendar AI Agent



\## 1. Team Roles \& Responsibilities

To fulfill the mandatory pair-work assignment criteria and maintain a clean integration workflow, tasks are split evenly across specific domains:

\* \*\*Student A (Infrastructure \& API Engineer):\*\* Responsible for Google Cloud Project setups, OAuth2 credential flows, writing the rigid integrations for Google APIs (Gmail fetching, Calendar reading/writing), and implementing the system-wide Dry-Run architecture.

\* \*\*Student B (Agent Logic \& LLM Engineer):\*\* Responsible for overarching Agent state-loops, prompt engineering, structured LLM information extraction, intent classification modeling, and building workflows for edge-case resolution (missing values or scheduled conflicts).



\## 2. Project Timeline \& Milestones

The development timeline spans exactly two weeks from the assignment prompt (May 25, 2026 – June 8, 2026):



| Phase | Core Activities | Assignment | Recommended Deadline | Status |

| :--- | :--- | :--- | :--- | :--- |

| \*\*Phase 1: Infra \& Security\*\* | Set up dedicated test account, map `.gitignore`, configure `uv` environments, and lock keys to variables. | Student A | May 28, 2026 | \*\*Completed\*\* |

| \*\*Phase 2: Scanning \& Extraction\*\* | Connect to Gmail API, build the mail-fetching skill, and draft initial LLM prompts for entity extraction. | Joint Effort | May 31, 2026 | \*\*Completed\*\* |

| \*\*Phase 3: Calendar \& Routing\*\* | Connect to Calendar API, develop conflict checks, script response logic for rejections and draft generation. | Student B | June 3, 2026 | \*\*In Progress\*\* |

| \*\*Phase 4: Agent Integration\*\* | Consolidate core loops in `main.py`, run E2E live tests with multi-language inputs, and check `AI\_PROCESSED` labels. | Joint Effort | June 5, 2026 | \*\*Pending\*\* |

| \*\*Phase 5: Docs \& Hand-in\*\* | Format project structures, complete the final `README.md`, sync git branches, and submit the final repository link. | Joint Effort | June 8, 2026 | \*\*Pending\*\* |



\## 3. Risk Management \& Mitigations

\* \*\*Risk:\*\* Accidental leakage of Google OAuth API secrets or user tokens onto public GitHub branches.

&#x20; \* \*Mitigation:\* Perform mandatory local `git status` inspections before compiling any code-commit or tracking updates to remote origins.

\* \*\*Risk:\*\* LLM failing to parse erratic or poorly punctuated date/time structures inside informal text bodies.

&#x20; \* \*Mitigation:\* Enforce a strict heuristic fallback framework within the agent. If the LLM confidence score drops below 100% regarding mandatory parameters, the agent will immediately route the request to an edge-case handler to build a safe draft reply rather than executing a faulty calendar entry.

