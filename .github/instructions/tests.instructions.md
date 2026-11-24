---
applyTo: "tests/**/*.py"
---
# Test rules
- One behaviour per test. Name tests `test_<what_should_happen>`.
- Use `pytest.approx` for floating-point values.
- Do not use random numbers or the clock in tests (tests must be repeatable).
