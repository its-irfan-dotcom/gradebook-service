
import pytest

from errors import ValidationError
from models import (
    Assessment,
    Mark,
    Student,
    parse_assessment,
    parse_mark,
    parse_number,
    parse_student,
    parse_text,
)


def test_numeric_string_is_accepted() -> None:
    assert parse_number("85.5", "score") == 85.5


def test_nonblank_text_is_stripped() -> None:
    assert parse_text("  Ali  ", "name") == "Ali"


def test_boolean_is_rejected_as_number() -> None:
    with pytest.raises(ValidationError):
        parse_number(True, "score")


def test_nan_is_rejected() -> None:
    with pytest.raises(ValidationError):
        parse_number(float("nan"), "score")


def test_zero_assessment_total_is_rejected() -> None:
    with pytest.raises(ValidationError):
        Assessment("a1", "Quiz", 20.0, 0.0)


def test_negative_mark_score_is_rejected() -> None:
    with pytest.raises(ValidationError):
        Mark("s1", "a1", -1.0)


def test_missing_student_field_is_rejected() -> None:
    with pytest.raises(ValidationError, match="name"):
        parse_student({"id": "s1"})


def test_non_dictionary_payload_is_rejected() -> None:
    with pytest.raises(ValidationError, match="payload"):
        parse_student(123)


def test_valid_assessment_payload_is_parsed() -> None:
    assessment = parse_assessment(
        {
            "id": "a1",
            "title": "Quiz",
            "weight": "20",
            "total": 100,
        }
    )

    assert assessment.id == "a1"
    assert assessment.title == "Quiz"
    assert assessment.weight == 20.0
    assert assessment.total == 100.0


def test_valid_student_payload_is_parsed() -> None:
    student = parse_student({"id": "s1", "name": "Ali"})

    assert student == Student("s1", "Ali")


def test_valid_mark_payload_is_parsed() -> None:
    mark = parse_mark(
        {"student": "s1", "assessment": "a1", "score": "75"}
    )

    assert mark.student == "s1"
    assert mark.assessment == "a1"
    assert mark.score == 75.0
