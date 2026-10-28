
from unittest.mock import Mock

import pytest

from errors import NotFoundError, ValidationError
from gradebook import add_mark


def make_state():
    return {
        "students": {
            "S1": {"id": "S1", "name": "Ali"},
        },
        "assessments": {
            "A1": {
                "id": "A1",
                "title": "Quiz",
                "weight": 10,
                "total": 20,
            },
        },
        "marks": [],
    }


def fixed_time():
    return "2026-10-12 09:00:00"


def test_valid_mark_is_stored_with_timestamp():
    state = make_state()
    mark = type(
        "Mark",
        (),
        {"student": "S1", "assessment": "A1", "score": 15},
    )()
    save = Mock()

    add_mark(state, mark, fixed_time, save)

    assert state["marks"] == [
        {
            "student": "S1",
            "assessment": "A1",
            "score": 15,
            "at": "2026-10-12 09:00:00",
        }
    ]


def test_valid_mark_calls_save_once():
    state = make_state()
    mark = type(
        "Mark",
        (),
        {"student": "S1", "assessment": "A1", "score": 15},
    )()
    save = Mock()

    add_mark(state, mark, fixed_time, save)

    save.assert_called_once_with()


@pytest.mark.parametrize(
    ("student", "assessment", "score", "error"),
    [
        pytest.param("S9", "A1", 15, NotFoundError, id="unknown-student"),
        pytest.param("S1", "A9", 15, NotFoundError, id="unknown-assessment"),
        pytest.param("S1", "A1", 25, ValidationError, id="score-too-high"),
    ],
)
def test_invalid_mark_is_rejected_without_saving(
    student, assessment, score, error
):
    state = make_state()
    mark = type(
        "Mark",
        (),
        {
            "student": student,
            "assessment": assessment,
            "score": score,
        },
    )()
    save = Mock()

    with pytest.raises(error):
        add_mark(state, mark, fixed_time, save)

    assert state["marks"] == []
    save.assert_not_called()
