
import datetime
import http.server
import json
import logging
import sys
from collections.abc import Callable
from typing import Any

from errors import (
    ConflictError,
    GradebookError,
    NotFoundError,
    ValidationError,
)
from models import parse_assessment, parse_mark, parse_student

DATA = "gradebook.json"
STATE: dict[str, Any] = {
    "students": {},
    "assessments": {},
    "marks": [],
}

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def load() -> None:
    global STATE

    try:
        with open(DATA, encoding="utf-8") as file:
            STATE = json.load(file)
    except FileNotFoundError:
        STATE = {"students": {}, "assessments": {}, "marks": []}


def save() -> None:
    with open(DATA, "w", encoding="utf-8") as file:
        json.dump(STATE, file)


def pct(sid: str) -> str:
    total = 0.0
    got = 0.0

    for mark in STATE["marks"]:
        if mark["student"] == sid:
            assessment = STATE["assessments"].get(mark["assessment"])
            if assessment:
                weight = float(assessment["weight"])
                assessment_total = float(assessment["total"])
                got += float(mark["score"]) * weight / assessment_total
                total += weight

    if total == 0:
        return "0"

    return str(round(got, 2))


class Handler(http.server.BaseHTTPRequestHandler):
    def log_message(self, format_string: str, *args: Any) -> None:
        logger.info(
            "%s - %s",
            self.address_string(),
            format_string % args,
        )

    def _send(self, code: int, obj: object) -> None:
        body = json.dumps(obj).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _handle(self, action: Callable[[], tuple[int, object]]) -> None:
        try:
            status, body = action()
            self._send(status, body)
        except ValidationError as exc:
            self._send(400, {"error": str(exc)})
        except NotFoundError as exc:
            self._send(404, {"error": str(exc)})
        except ConflictError as exc:
            self._send(409, {"error": str(exc)})
        except GradebookError as exc:
            self._send(400, {"error": str(exc)})
        except Exception:
            logger.exception(
                "Unexpected error while handling %s",
                self.path,
            )
            self._send(500, {"error": "internal error"})

    def _get(self) -> tuple[int, object]:
        if self.path == "/students":
            return 200, list(STATE["students"].values())

        if self.path.startswith("/students/"):
            sid = self.path[len("/students/"):]

            if not sid or "/" in sid:
                raise NotFoundError("student not found")

            student = STATE["students"].get(sid)
            if student is None:
                raise NotFoundError("student not found")

            result = dict(student)
            result["percentage"] = pct(sid)
            return 200, result

        if self.path == "/assessments":
            return 200, list(STATE["assessments"].values())

        if self.path == "/report":
            report = [
                {
                    "id": sid,
                    "name": student["name"],
                    "pct": pct(sid),
                }
                for sid, student in STATE["students"].items()
            ]
            return 200, report

        raise NotFoundError("unknown endpoint")

    def _post(self) -> tuple[int, object]:
        try:
            length = int(self.headers.get("Content-Length", "0"))
        except ValueError as exc:
            raise ValidationError(
                "Content-Length must be a number"
            ) from exc

        if length <= 0:
            raise ValidationError("request body is required")

        raw = self.rfile.read(length)

        try:
            payload = json.loads(raw)
        except (json.JSONDecodeError, UnicodeDecodeError) as exc:
            raise ValidationError("bad JSON") from exc

        if self.path == "/students":
            student = parse_student(payload)
            sid = student.id

            if sid in STATE["students"]:
                raise ConflictError("student already exists")

            record: dict[str, Any] = {
                "id": student.id,
                "name": student.name,
                "joined": str(datetime.datetime.now()),
            }

            STATE["students"][sid] = record
            save()
            return 201, record

        if self.path == "/assessments":
            assessment = parse_assessment(payload)
            aid = assessment.id

            if aid in STATE["assessments"]:
                raise ConflictError("assessment already exists")

            assessment_record: dict[str, Any] = {
                "id": assessment.id,
                "title": assessment.title,
                "weight": assessment.weight,
                "total": assessment.total,
            }

            STATE["assessments"][aid] = assessment_record
            save()
            return 201, assessment_record

        if self.path == "/marks":
            mark = parse_mark(payload)

            if mark.student not in STATE["students"]:
                raise NotFoundError("student not found")

            assessment = STATE["assessments"].get(mark.assessment)
            if assessment is None:
                raise NotFoundError("assessment not found")

            if mark.score > float(assessment["total"]):
                raise ValidationError(
                    "score cannot exceed assessment total"
                )

            mark_record: dict[str, Any] = {
                "student": mark.student,
                "assessment": mark.assessment,
                "score": mark.score,
                "at": str(datetime.datetime.now()),
            }

            STATE["marks"].append(mark_record)
            save()
            logger.info(
                "Recorded mark for student %s, score %s",
                mark.student,
                mark.score,
            )
            return 201, {"ok": True}

        raise NotFoundError("unknown endpoint")

    def do_GET(self) -> None:
        self._handle(self._get)

    def do_POST(self) -> None:
        self._handle(self._post)


def main(argv: list[str] | None = None) -> None:
    if argv is None:
        argv = sys.argv

    port = 8000

    if len(argv) > 1:
        try:
            port = int(argv[1])
        except ValueError as exc:
            raise SystemExit(
                "Port must be a whole number between 1 and 65535"
            ) from exc

    if not 1 <= port <= 65535:
        raise SystemExit(
            "Port must be a whole number between 1 and 65535"
        )

    load()
    logger.info("Gradebook service listening on port %s", port)
    server = http.server.HTTPServer(("", port), Handler)
    server.serve_forever()


if __name__ == "__main__":
    main()
