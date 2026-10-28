
import pytest
import gradebook


def test_student_with_no_marks_has_zero_percentage(loaded):
    # Arrange: loaded provides a student with no marks.

    # Act
    result = gradebook.pct("S1")

    # Assert
    assert result == "0"


def test_student_with_one_mark_gets_correct_percentage(loaded):
    # Arrange
    loaded["marks"].append({
        "student": "S1",
        "assessment": "A1",
        "score": 15,
    })

    # Act
    result = gradebook.pct("S1")

    # Assert
    assert result == "7.5"


def test_mark_for_unknown_assessment_is_ignored(loaded):
    # Arrange
    loaded["marks"].append({
        "student": "S1",
        "assessment": "UNKNOWN",
        "score": 15,
    })

    # Act
    result = gradebook.pct("S1")

    # Assert
    assert result == "0"
