# Castle Busters - instructions for every Copilot agent

## Project
Castle Busters is a small Python 3.11+ game (like a catapult-and-castle game).
- Game rules live in `castle_busters/` (`physics.py`, `castle.py`, `scoring.py`).
- `game.py` is the only file that draws on screen (turtle). Keep game rules out of it.
- Tests live in `tests/` and use pytest.

## How to build and test
- Install: `pip install -r requirements-dev.txt`
- Test: `python -m pytest -q`
- Lint: `ruff check .`

## Rules for agents
1. PLAN FIRST. Before changing code, write a short plan (files, steps, tests, risks).
2. Every new rule or function needs at least one pytest test.
3. Never change files in `.github/workflows/` or `.github/CODEOWNERS` unless the task says so.
4. Never add new third-party packages without asking.
5. Read `docs/agent-state/DECISIONS.md` before you start. Do not go against a recorded decision.
6. When you finish, add one line to `docs/agent-state/PROGRESS.md`.
