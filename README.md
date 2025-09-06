# Pinkman — Product Spec & Design (Draft)

This document is the living blueprint for the app. We’ll finalize it together before writing any code. Sections marked with [TBD] are awaiting decisions.

## 1) Vision & Problem
- One-line vision: A minimal Streamlit front-end for AI applications—a single-page chat UI with a top "pinkman" banner.
- Problem statement: Provide a dead-simple chat front-end that connects to an AI agent backend, with zero setup and no account.
- Value proposition (why this, why now): Accelerates prototyping and demos by removing UX scaffolding; focus on the agent logic.

## 2) Users & Personas
- Primary user(s): AI developer
- Secondary stakeholders: App user
- Key pains and needs: Quickly prototype with LangChain, CrewAI, and the like, to build AI apps quickly. It is neater than a CLI and could output more than just text!

## 3) Goals & Non-Goals
- Goals (what success looks like):
  - Single-page chat where the user types a message and gets a reply in a feed.
  - Prominent top banner with the word "pinkman".
  - Zero settings and no user login.
  - Keep setup friction low (run locally with minimal config).
  - Clean, responsive, accessible UI with sensible defaults.
- Non-goals (explicitly out of scope for v1):
  - Settings panels or model controls.
  - Authentication, user accounts, or multi-tenant features.
  - Admin dashboards and advanced analytics.
  - Offline packaging and installers.

## 4) Scope (v1)
- In scope features (must-have):
  - Single-page chat interface (feed of messages with roles: user/assistant) beneath a top banner labeled "pinkman".
  - Message input box with Send and Enter-to-send (Shift+Enter for newline).
  - Backend agent integration via a simple Python interface.
  - Clear conversation button (resets history).
  - Conversation history stored in session (per browser session) with a length cap.
- Nice-to-haves (v1.1 or later):
  - Streaming responses (token-by-token), cancel generation.
  - Markdown rendering (including code blocks with copy and syntax highlighting).
  - Local persistence (optional) and export/import conversation JSON.
  - Keyboard shortcuts (Ctrl/Cmd+K to clear, etc.).

## 5) Success Metrics
- North star metric: Time-to-first-reply (TTFR) < 2s using the default backend agent locally.
- Supporting metrics (performance, quality):
  - p95 render time for sending and displaying a reply < 250ms (non-LLM path).
  - Zero console errors in normal flows.
  - Accessibility checks pass for color contrast and focus management.

## 6) Functional Requirements
List the user-facing capabilities and system behaviors.
- Authentication & authorization: None for v1.
- UI layout: Top banner with the word "pinkman"; chat feed underneath; input at bottom.
- Chat feed: Display ordered list of messages with role badges and timestamps.
- Message input: Multiline text area, Enter to send, Shift+Enter for newline.
- Backend agent: Interface to produce assistant replies from a list of messages.
- Conversation state: Maintain history in memory (per-session) with a length cap.
- Clear chat: Action to reset the session state.
- Error handling: Show inline error message if backend agent fails.
- Integrations: Optional LLM/API provider can be wired behind the backend agent interface (no settings UI).
- Admin / moderation: None in v1.

## 7) Non-Functional Requirements
- Performance: Local non-LLM reply path responds within 200ms on modern hardware.
- Reliability/Availability: Single-user local app; no server uptime target for v1.
- Security & Privacy: No server-side data persistence in v1; API keys stored locally via .env only if LLM used.
- Compliance: N/A for local v1; re-evaluate if hosted.
- Accessibility: Respect prefers-reduced-motion; proper focus order; contrast AA for text.
- Internationalization/Localization: English only in v1.
- Observability: Minimal console logging; no telemetry in v1 (local).

## 8) System Design
- High-level architecture (diagram placeholder):
  - UI: Streamlit single-page app rendering chat feed and input.
  - Backend agent: Python module implementing a simple contract (see below). Could call local logic or external APIs.
  - Storage: In-memory via Streamlit session_state; optional local JSON export (later).
  - Integrations: Optional LLM providers via HTTP APIs (wired inside the backend agent).
- Key flows:
  - Send message: User enters text -> append to session history -> call backend agent -> display reply -> update feed.
  - Clear chat: Reset session_state for messages.
- Data model (preliminary):
  - Message: { id, role: 'user'|'assistant'|'system', content: str, ts: datetime }
  - Conversation: { id, messages: [Message] }
- Backend agent contract (draft):
  - Inputs:
    - messages: list[dict] where dict = {"role": str, "content": str}
    - context (optional): dict for future extensibility
  - Output:
    - reply: str (v1); future: iterable/stream of chunks
  - Error modes:
    - Raises exception on failure (handled by UI with inline error)
  - Performance:
    - Synchronous call returns < 1s for local path
  - Edge cases:
    - Empty/whitespace input → ignore and do nothing
    - Very long input → truncate or summarize before sending
    - Backend timeout → show error and allow retry

## 9) UX & Content
- Primary jobs-to-be-done and use cases: Quick back-and-forth chat with an AI agent.
- Screen list / navigation map: Single view: Top banner ("pinkman") → chat timeline (center) → input bar (bottom). Clear button in header.
- Rough wireframes (textual notes):
  - Header: pinkman | Clear
  - Feed: Bubbled messages (assistant on left, user on right), timestamps
  - Input: Multiline textarea + Send button; hint (Enter to send, Shift+Enter newline)
- Content strategy & tone: Neutral, concise UI copy; avoid jargon.
- Accessibility considerations: Focus returns to input after send; labels for buttons; live region for future streaming.

## 10) Tech Stack Options (to choose)
Pick one path for v1, based on constraints and familiarity.
- Web (full TypeScript): Next.js (App Router) + React + Tailwind; API via Next.js Route Handlers or separate Node/Express; DB: Postgres + Prisma.
- Web (Python backend): React/Vite + FastAPI; DB: Postgres + SQLModel/SQLAlchemy.
- Mobile: React Native (Expo) or Flutter; backend as above.
- Desktop: Tauri or Electron; backend optional (local sync or remote API).
- Auth: Clerk/Auth0/NextAuth/OAuth 2.0 + OIDC.
- Infra: Docker dev containers; CI GitHub Actions; deploy to Vercel/Render/Fly.io/AWS.

Decision: Web (Streamlit) + Python 3.11; Backend agent: start simple (echo/template) with optional LLM provider wired inside the agent. No settings or login in v1.

## 11) DevEx, Quality, and Delivery
- Local dev environment: Python 3.11+, pip/uv/poetry; .env handling (python-dotenv) if using LLM.
- Code quality: Ruff + Black; mypy for typing; pre-commit hooks optional.
- Testing strategy: unit tests for reply engine; lightweight snapshot tests for rendering functions; smoke test launching Streamlit.
- CI/CD: [TBD] (run tests and ruff/black on PR); optional build of a docker image.
- Environments: local only for v1; consider lightweight hosting later.
- Release/versioning: Git tags for milestones.

## 12) Data & Privacy
- Data collected and purpose: None server-side; local session history only. If LLM used, prompts/responses sent to provider per their policy.
- Retention policy: Session-only in v1; optional export/import in later versions.
- Anonymization / minimization: Send minimal context to providers; allow disabling sending past messages.
- User controls (export/delete): Clear chat in v1; export/import later.

## 13) Risks & Mitigations
- Risk: LLM API cost or rate limits. → Mitigation: Default to local echo/template engine; add configurable rate limit.
- Risk: Session memory growth. → Mitigation: Cap history length; provide Clear; compress/summarize later.
- Risk: Provider outages. → Mitigation: Fallback to alternate provider or local engine.

## 14) Timeline & Milestones (Draft)
- Milestone 1: Spec locked; Streamlit skeleton with chat UI and echo replies. [1–2 days]
- Milestone 2: Optional LLM integration behind config; markdown rendering; clear chat. [2–3 days]
- Milestone 3: Polish (a11y, shortcuts), light tests, README runbook. [1–2 days]
- Milestone 4: Optional packaging/hosting guidance. [TBD]

## 15) Open Questions
- Which backend agent for v1? (echo/template vs. OpenAI/Azure/OpenRouter vs. local model)
- Do we need streaming responses in v1?
- Any need for conversation export/import in v1?

## 16) Decision Log
| Date       | Decision                                                                 | Context |
|------------|--------------------------------------------------------------------------|---------|
| 2025-09-06 | Choose Streamlit + Python; minimal OpenChat-style chat UI for v1.        | User preference |
| 2025-09-06 | Acts as a front-end for AI apps; single page with top "pinkman" banner; no settings/login. | Clarified scope |

---

## Quick Questions to Finalize v1
Please answer these to converge the spec quickly:
1) What type of app do you want first: web, mobile, desktop, or CLI?
2) Who are the primary users? Any specific industry or region?
3) Top 3 problems it must solve in v1?
4) Must-have features for v1, in order of priority?
5) Any required integrations (payments, email, storage, third-party APIs)?
6) Do you need authentication? If yes, which providers (email, Google, Microsoft, others)?
7) Any regulatory or data privacy constraints (GDPR/CCPA/HIPAA)?
8) Target timeline for MVP and any deadlines?
9) Preferred stack/language (TypeScript/Node, Python, etc.)?
10) Monetization model (free, subscription, one-time, internal-only)?

Once we have these answers, I’ll fill in the spec (architecture, data model, API contracts, and UX outline) and prepare a delivery plan. 

## How to run (local)
These commands are for Windows PowerShell.

1) Create and activate a virtual environment (optional but recommended)
```powershell
python -m venv .venv; .\.venv\Scripts\Activate.ps1
```

2) Install dependencies
```powershell
pip install -r requirements.txt
```

3) Launch the app
```powershell
streamlit run app.py
```

If you later wire an external LLM, you may add a .env file for API keys and load it in `pinkman/agent.py` using python-dotenv.