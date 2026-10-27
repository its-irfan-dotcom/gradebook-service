# Task 2 — Experiments and Observations

1. The GET endpoints return student, assessment, and report data.
2. Sending a student request without an ID returns an error message.
3. Sending malformed JSON returns a `bad json` error.
4. The current implementation returns HTTP status code 200 for these errors instead of an appropriate error status code.
5. These experiments show why input validation and proper exception handling are important.