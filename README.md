
# Vision & Problem
- One-line vision: A lightweight Streamlit front end for AI apps—a single-page chat interface.
- Problem statement: Offer a no-frills chat UI that connects to an AI agent backend, with zero configuration and no sign-in.
- Value proposition (why this, why now): Speed up demos and prototypes by cutting UX boilerplate so you can focus on agent logic.
- Quickly iterate with tools like LangChain or CrewAI; cleaner than a CLI and capable of richer outputs than plain text.

## Run
- Ensure Python 3.11+ and install dependencies:
	- Use your environment manager, then install from `requirements.txt`.
- Start the app:
	- Run Streamlit and open the provided local URL.

## Logging configuration
- Create `config/.env` with:
	- `LOG_ENABLED=true|false`
	- `LOG_FILE=log.txt` (path to a writable text file)
- When enabled, each message is appended as a single line:
	- `[YYYY-MM-DDTHH:MM:SSZ] role: content`
- If `config/.env` is missing, the app will raise an error at startup when the logger initializes.

