
## Backend AI Logic
- The backend logic is implemented in `ai.py` as the `AI` class.
- To generate replies, instantiate `AI` and call its `generate_reply` method.

# Vision & Problem
- One-line vision: A lightweight Streamlit front end for AI apps—a single-page chat interface.
- Problem statement: Offer a no-frills chat UI that connects to an AI agent backend, with zero configuration and no sign-in.
- Value proposition (why this, why now): Speed up demos and prototypes by cutting UX boilerplate so you can focus on agent logic.
- Quickly iterate with tools like LangChain or CrewAI; cleaner than a CLI and capable of richer outputs than plain text.

## Run
- Ensure Python 3.11+ and install dependencies from `requirements.txt`.
- Create `config/.env` by copying `config/.env.example` and fill in values (at minimum `OPENAI_API_KEY` and `GPT_MODEL`).
- Start the app with Streamlit and open the provided local URL.

## Tests
- Install dev dependencies (pytest is in `requirements.txt`).
- Run tests from the project root:

Windows (cmd.exe):

```
pip install -r requirements.txt
pytest -q
```

Windows (PowerShell):
1) Install dev deps (pytest):
```
pip install -r requirements.txt
pytest -q
```

Integration test (real OpenAI client):

- By default, tests use a stubbed client to stay fast and deterministic.
- To run an optional integration test against the real OpenAI API:
	- Ensure OPENAI_API_KEY is set in config/.env or environment.
	- Enable the guard:
		- Windows cmd.exe: set RUN_REAL_OPENAI_TESTS=1
	- Then run tests: pytest -q
	- The guarded test asserts the reply mentions Cairo.

- Ensure `config/.env` exists with at least `OPENAI_API_KEY` and `GPT_MODEL` set (dummy values are fine for tests).

## Logging configuration
- Create `config/.env` with:
	- `LOG_ENABLED=true|false`
	- `LOG_FILE=log.txt` (path to a writable text file)
- When enabled, each message is appended as a single line:
	- `[YYYY-MM-DDTHH:MM:SSZ] role: content`
- If `config/.env` is missing, the app will raise an error at startup when the logger initializes.

## Contributing / Git workflow

This repository may protect the `main` branch. Don’t push directly to `main`.

1) Create a branch:
	- `git checkout -b feat/your-change`
2) Commit on your branch:
	- `git add -A`
	- `git commit -m "feat: your change"`
3) Push your branch:
	- `git push -u origin feat/your-change`
4) Open a Pull Request targeting `main` on GitHub.

Notes:
- `config/.env` is gitignored; commit `config/.env.example` (no secrets) instead.
- If push is rejected by a ruleset, ensure your branch is up to date and/or signed as required:
  - `git fetch origin`
  - `git rebase origin/main`
  - `git push -u origin feat/your-change`

