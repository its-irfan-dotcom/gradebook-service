
from unittest.mock import Mock

import pytest

from errors import ConflictError, ValidationError
from gradebook import add_assessment


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


def make_assessment(assessment_id, title, weight, total):
    return type(
        "Assessment",
        (),
        {
            "id": assessment_id,
            "title": title,
            "weight": weight,
            "total": total,
        },
    )()


def test_valid_assessment_is_stored():
    state = make_state()
    assessment = make_assessment("A2", "Midterm", 40, 100)
    save = Mock()

    result = add_assessment(state, assessment, save)

    assert result == {
        "id": "A2",
        "title": "Midterm",
        "weight": 40,
        "total": 100,
    }
    assert state["assessments"]["A2"] == result


def test_valid_assessment_calls_save_once():
    state = make_state()
    assessment = make_assessment("A2", "Midterm", 40, 100)
    save = Mock()

    add_assessment(state, assessment, save)

    save.assert_called_once_with()


def test_total_weight_above_100_is_rejected():
    state = make_state()
    assessment = make_assessment("A2", "Final", 91, 100)
    save = Mock()

    with pytest.raises(ValidationError):
        add_assessment(state, assessment, save)

    assert "A2" not in state["assessments"]
    save.assert_not_called()


def test_duplicate_assessment_id_is_rejected():
    state = make_state()
    assessment = make_assessment("A1", "Another Quiz", 20, 50)
    save = Mock()

    with pytest.raises(ConflictError):
        add_assessment(state, assessment, save)

    assert state["assessments"]["A1"]["title"] == "Quiz"
    save.assert_not_called()
