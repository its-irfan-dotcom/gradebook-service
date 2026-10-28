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


# Lab 05 — Test-Driven Development and Boundary Cases

## Task 1 — Testing and Coverage Setup

- Tools installed: pytest, hypothesis, coverage, ruff, mypy
- Total coverage: 53%
- File with the lowest coverage: gradebook.py (38%)


## Task 2 — Test-Driven Development

### Cycle 1
- Test: Empty existing weights with new weight 50.
- Result: Passed after implementing the minimum function.

### Cycle 2
- Test: Existing weight 60 plus new weight 50.
- Expected: ValidationError with 100 in the message.
- Initial failure message: [Paste actual failure message]

### Cycle 3
- Test: Existing weight 60 plus new weight 40.
- Result: [Record whether it failed first or passed immediately.]

### Cycle 4
- Test: Decimal weights totaling 100.
- Initial failure message: [Paste actual failure message]
- Fix: Added a tolerance of 1e-9.

# Task 5
The full test suite has 58% code coverage. Coverage shows which code was executed, but it cannot tell me whether my tests correctly check the results or detect every bug. The `main()` function in `gradebook.py` has no direct test.


Task 6 mutation test: `test_score_boundaries` failed when the score validation operator was changed from `>` to `>=`. This confirms that a score equal to the assessment total must be accepted.

Hypothesis found that adding multiple marks for the same student and assessment can make the percentage exceed the assessment weight. The defect is that `add_mark()` counts duplicate marks instead of replacing the previous mark.

**Task 7 — Property-Based Testing**

- Hypothesis failing example: `scores=[1, 20]`
- Actual percentage: 10.5
- Expected maximum percentage: 10
- Defect: `add_mark()` stores duplicate marks for the same student and assessment. The `pct()` function counts both marks, allowing the percentage to exceed the assessment weight.