
import pytest

import gradebook


@pytest.mark.parametrize(
    ("marks", "expected"),
    [
        pytest.param([], "0", id="no-marks"),
        pytest.param(
            [{"student": "S1", "assessment": "A1", "score": 15}],
            "7.5",
            id="a1-score-15",
        ),
        pytest.param(
            [{"student": "S1", "assessment": "A1", "score": 20}],
            "10.0",
            id="a1-score-20",
        ),
        pytest.param(
            [{"student": "S1", "assessment": "A1", "score": 0}],
            "0.0",
            id="a1-score-zero",
        ),
        pytest.param(
            [
                {"student": "S1", "assessment": "A1", "score": 15},
                {"student": "S1", "assessment": "A2", "score": 40},
            ],
            "31.5",
            id="a1-and-a2",
        ),
    ],
)
def test_student_percentage(loaded, marks, expected):
    # Arrange
    loaded["marks"] = marks

    # Act
    result = gradebook.pct("S1")

    # Assert
    assert result == expected


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
