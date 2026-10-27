
import math
from dataclasses import dataclass
from typing import cast

from errors import ValidationError


@dataclass(frozen=True)
class Student:
    id: str
    name: str

    def __post_init__(self) -> None:
        if not self.id.strip():
            raise ValidationError("id must be a non-blank string")
        if not self.name.strip():
            raise ValidationError("name must be a non-blank string")


@dataclass(frozen=True)
class Assessment:
    id: str
    title: str
    weight: float
    total: float

    def __post_init__(self) -> None:
        if not self.id.strip():
            raise ValidationError("id must be a non-blank string")
        if not self.title.strip():
            raise ValidationError("title must be a non-blank string")
        if not math.isfinite(self.weight) or not 0 <= self.weight <= 100:
            raise ValidationError("weight must be between 0 and 100")
        if not math.isfinite(self.total) or self.total <= 0:
            raise ValidationError("total must be greater than 0")


@dataclass(frozen=True)
class Mark:
    student: str
    assessment: str
    score: float

    def __post_init__(self) -> None:
        if not self.student.strip():
            raise ValidationError("student must be a non-blank string")
        if not self.assessment.strip():
            raise ValidationError("assessment must be a non-blank string")
        if not math.isfinite(self.score) or self.score < 0:
            raise ValidationError("score must be a non-negative finite number")


def parse_number(raw: object, field: str) -> float:
    if isinstance(raw, bool):
        raise ValidationError(f"{field} must be a finite number")

    if isinstance(raw, (int, float)):
        value = float(raw)
    elif isinstance(raw, str):
        try:
            value = float(raw.strip())
        except ValueError as exc:
            raise ValidationError(f"{field} must be a number") from exc
    else:
        raise ValidationError(f"{field} must be a number")

    if not math.isfinite(value):
        raise ValidationError(f"{field} must be finite")

    return value


def parse_text(raw: object, field: str) -> str:
    if not isinstance(raw, str) or not raw.strip():
        raise ValidationError(f"{field} must be a non-blank string")
    return raw.strip()


def _payload_dict(payload: object) -> dict[str, object]:
    if not isinstance(payload, dict):
        raise ValidationError("payload must be an object")
    return cast(dict[str, object], payload)


def parse_student(payload: object) -> Student:
    data = _payload_dict(payload)
    return Student(
        id=parse_text(data.get("id"), "id"),
        name=parse_text(data.get("name"), "name"),
    )


def parse_assessment(payload: object) -> Assessment:
    data = _payload_dict(payload)
    return Assessment(
        id=parse_text(data.get("id"), "id"),
        title=parse_text(data.get("title"), "title"),
        weight=parse_number(data.get("weight"), "weight"),
        total=parse_number(data.get("total"), "total"),
    )


def parse_mark(payload: object) -> Mark:
    data = _payload_dict(payload)
    return Mark(
        student=parse_text(data.get("student"), "student"),
        assessment=parse_text(data.get("assessment"), "assessment"),
        score=parse_number(data.get("score"), "score"),
    )
