# Task 2 — Experiments and Observations

1. The GET endpoints return student, assessment, and report data.
2. Sending a student request without an ID returns an error message.
3. Sending malformed JSON returns a `bad json` error.
4. The current implementation returns HTTP status code 200 for these errors instead of an appropriate error status code.
5. These experiments show why input validation and proper exception handling are important.

# Lab 04 — Task 8: Test Failure Experiment

## Intentional failure

Changed `/` to `*` in `pct()` temporarily.

Pytest summary: **[paste the exact final summary line from your terminal here]**

Restored the original `/` operator after the experiment and reran the tests.

## Test doubles

- **Stub:** `tests/test_add_mark.py` uses a fixed clock that always returns `"2026-10-12 09:00:00"`, making the timestamp predictable.
- **Fake:** The tests use a simple dictionary as the gradebook state, so tests can check changes without using the real global state.
- **Mock:** `Mock()` replaces `save()` so tests can verify that saving happens exactly once for a valid mark and never for an invalid mark.

## Why not mock?

- **`pct()`:** It is the logic being tested, so it should run normally to prove that the calculation is correct.
- **File in Task 5:** `tmp_path` provides a real temporary file, allowing `load()` and `save()` to be tested without mocking file operations.

# Lab 05 — Test-Driven Development and Boundary Cases

## Task 1 — Testing and Coverage Setup

- Tools installed: pytest, hypothesis, coverage, ruff, mypy
- Total coverage: Pending coverage report
- File with the lowest coverage: Pending coverage report
