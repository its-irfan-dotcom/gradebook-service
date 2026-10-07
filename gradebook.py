import datetime
import http.server
import json
import logging
import sys
from typing import Any, Callable

from errors import ConflictError, NotFoundError, ValidationError
from models import parse_assessment, parse_mark, parse_student


DATA = "gradebook.json"

STATE: dict[str, Any] = {
    "students": {},
    "assessments": {},
    "marks": [],
}


def load() -> None:
    global STATE

    try:
        with open(DATA, encoding="utf-8") as file:
            STATE = json.load(file)
    except FileNotFoundError:
        STATE = {
            "students": {},
            "assessments": {},
            "marks": [],
        }


def save() -> None:
    with open(DATA, "w", encoding="utf-8") as file:
        json.dump(STATE, file)


def pct(sid: str) -> str:
    total = 0.0
    got = 0.0

    for mark in STATE["marks"]:
        if mark["student"] == sid:
            assessment = STATE["assessments"].get(mark["assessment"])

            if assessment is not None:
                score = float(mark["score"])
                weight = float(assessment["weight"])
                assessment_total = float(assessment["total"])

                got = got + score * weight / assessment_total
                total = total + weight

    if total == 0:
        return "0"

    return str(round(got, 2))


class Handler(http.server.BaseHTTPRequestHandler):

    def log_message(self, format: str, *args: object) -> None:
        logging.info(format, *args)

    def _send(self, code: int, obj: object) -> None:
        body = json.dumps(obj).encode()

        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _body(self) -> dict[str, object]:
        content_length = self.headers.get("Content-Length")

        if content_length is None:
            raise ValidationError("Content-Length is required")

        try:
            length = int(content_length)
        except ValueError:
            raise ValidationError("Content-Length must be a number") from None

        if length < 0:
            raise ValidationError("Content-Length must be a number")

        raw = self.rfile.read(length)

        try:
            payload = json.loads(raw)
        except (json.JSONDecodeError, UnicodeDecodeError):
            raise ValidationError("body must be valid JSON") from None

        if not isinstance(payload, dict):
            raise ValidationError("body must be a JSON object")

        return {str(key): value for key, value in payload.items()}

    def _dispatch(
        self,
        action: Callable[[], tuple[int, object]],
    ) -> None:
        try:
            status, body = action()
        except ValidationError as error:
            self._send(400, {"error": str(error)})
        except ConflictError as error:
            self._send(409, {"error": str(error)})
        except NotFoundError as error:
            self._send(404, {"error": str(error)})
        except Exception:
            logging.exception("unexpected error")
            self._send(500, {"error": "internal error"})
        else:
            self._send(status, body)

    def _get(self) -> tuple[int, object]:
        if self.path == "/students":
            return 200, list(STATE["students"].values())

        if self.path.startswith("/students/"):
            sid = self.path[len("/students/"):]

            if not sid or "/" in sid:
                raise NotFoundError("student not found")

            if sid not in STATE["students"]:
                raise NotFoundError("student not found")

            student = dict(STATE["students"][sid])
            student["percentage"] = pct(sid)

            return 200, student

        if self.path == "/assessments":
            return 200, list(STATE["assessments"].values())

        if self.path == "/report":
            output = []

            for sid in STATE["students"]:
                output.append(
                    {
                        "id": sid,
                        "name": STATE["students"][sid]["name"],
                        "pct": pct(sid),
                    }
                )

            return 200, output

        raise NotFoundError("route not found")

    def _post(self) -> tuple[int, object]:
        data = self._body()

        if self.path == "/students":
            student = parse_student(data)

            if student.id in STATE["students"]:
                raise ConflictError("student already exists")

            record = {
                "id": student.id,
                "name": student.name,
                "joined": str(datetime.datetime.now()),
            }

            STATE["students"][student.id] = record
            save()

            return 200, record

        if self.path == "/assessments":
            assessment = parse_assessment(data)

            if assessment.id in STATE["assessments"]:
                raise ConflictError("assessment already exists")

            record = {
                "id": assessment.id,
                "title": assessment.title,
                "weight": data["weight"],
                "total": data["total"],
            }

            STATE["assessments"][assessment.id] = record
            save()

            return 200, record

        if self.path == "/marks":
            mark = parse_mark(data)

            if mark.student not in STATE["students"]:
                raise NotFoundError("student not found")

            if mark.assessment not in STATE["assessments"]:
                raise NotFoundError("assessment not found")

            assessment = STATE["assessments"][mark.assessment]
            assessment_total = float(assessment["total"])

            if mark.score > assessment_total:
                raise ValidationError("score must not exceed total")

            record = {
                "student": mark.student,
                "assessment": mark.assessment,
                "score": data["score"],
                "at": str(datetime.datetime.now()),
            }

            STATE["marks"].append(record)
            save()

            logging.info(
                "recorded mark for %s score %s",
                mark.student,
                mark.score,
            )

            return 200, {"ok": True}

        raise NotFoundError("route not found")

    def do_GET(self) -> None:
        self._dispatch(self._get)

    def do_POST(self) -> None:
        self._dispatch(self._post)


def main(argv: list[str] | None = None) -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
    )

    arguments = sys.argv if argv is None else argv

    try:
        load()
    except json.JSONDecodeError as error:
        raise SystemExit(
            f"invalid gradebook.json: {error.msg}"
        ) from None

    port = 8000

    if len(arguments) > 1:
        try:
            port = int(arguments[1])
        except ValueError:
            raise SystemExit(
                "port must be a whole number from 1 to 65535"
            ) from None

        if port < 1 or port > 65535:
            raise SystemExit(
                "port must be a whole number from 1 to 65535"
            )

    logging.info("gradebook on %s", port)

    server = http.server.HTTPServer(("", port), Handler)
    server.serve_forever()


if __name__ == "__main__":
    main()