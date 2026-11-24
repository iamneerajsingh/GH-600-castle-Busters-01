# Goal

Add optional wind to shots so horizontal drift affects the boulder's flight without changing zero-wind results.

# Inputs

- Issue #1 and this plan, linked in the implementation PR.
- `castle_busters/physics.py` and `tests/test_physics.py`.
- Decision D2 in `docs/agent-state/DECISIONS.md`: gravity remains 9.8.
- Test conventions in `.github/instructions/tests.instructions.md`.

# Steps

1. **test-guardian — `tests/test_physics.py`:** Add deterministic tests for negative wind (headwind), positive wind (tailwind), and default and explicit zero wind, including the horizontal drift formula and unchanged vertical position.
2. **test-guardian — `tests/test_physics.py`:** Test that wind affects landing distance and trajectory consistently while flight time remains unchanged, and that existing two-argument shots and zero-wind results remain compatible.
3. **game-dev — `castle_busters/physics.py`:** Add a `wind` field in metres per second to `Shot`, defaulting to zero, after the existing fields so existing callers remain compatible.
4. **game-dev — `castle_busters/physics.py`:** Calculate horizontal position as `power * cos(angle) * t + wind * t`; leave vertical motion, gravity, and the existing shot validation unchanged.
5. **test-guardian — `tests/test_physics.py`:** Run the targeted physics tests, then the full test suite and Ruff; review the resulting changes and link this plan in the implementation PR.

# Tests

- Run `python -m pytest -q tests/test_physics.py` for focused coverage.
- Run `python -m pytest -q` for regression coverage and `ruff check .` for lint.
- Use exact equality to compare zero-wind results against the previous formula and default shots; use `pytest.approx` for other floating-point expectations.

# Success criteria

- Headwind and tailwind change horizontal position by `wind * t`, with no change to vertical position or flight time.
- Default and explicit zero wind reproduce existing positions exactly; existing callers and tests continue to work.
- Landing distance and trajectory reflect wind, gravity remains 9.8, all tests pass, and Ruff is clean.
- The implementation PR links this plan and receives the required review.

# Risks and what needs human approval

- Medium risk: wind changes game physics and derived landing distances; a human must approve this plan before implementation and review the implementation PR.
- No changes to `game.py`, `scoring.py`, or `.github/workflows/`; no new third-party packages without human approval.

# Hand-off

- **test-guardian:** Steps 1, 2, and 5.
- **game-dev:** Steps 3 and 4.
