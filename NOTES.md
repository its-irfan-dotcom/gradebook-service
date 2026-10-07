# Task 2 - Failing Well

## (a) GET /students/NOPE

Command:

curl.exe -i http://localhost:8000/students/NOPE

Result:

HTTP 200 with {"error":"not found"}

Expected after fixing:

HTTP 404


## (b) POST /students with body 5

Command:

curl.exe -i -X POST http://localhost:8000/students -d "5"

Result:

No proper HTTP response / server traceback.

Expected after fixing:

HTTP 400


## (c) Invalid score "abc"

Commands:

curl.exe -i -X POST http://localhost:8000/students -d '{"id":"S1","name":"Ayesha"}'

curl.exe -i -X POST http://localhost:8000/assessments -d '{"id":"A1","title":"Quiz 1","weight":"10","total":"20"}'

curl.exe -i -X POST http://localhost:8000/marks -d '{"student":"S1","assessment":"A1","score":"abc"}'

curl.exe -i http://localhost:8000/students/S1

Result:

The invalid score is accepted with HTTP 200. Later percentage calculation
causes a ValueError because "abc" cannot be converted to float.


## (d) Assessment total "0"

Result:

The old service accepts total 0 and later crashes with ZeroDivisionError
when calculating the report.


## (e) Mark for nonexistent assessment

Result:

The old service accepts the mark when the student exists, even though the
assessment does not exist.


## Why gradebook.json was deleted

gradebook.json was deleted to reset the persistent state of the service.
This ensured that each experiment started with clean data.


## Bare except locations

The bare except statements were found at:

- Line 18
- Line 26
- Line 79