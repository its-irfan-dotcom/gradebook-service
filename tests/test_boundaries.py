
import pytest

from errors import ValidationError
from gradebook import add_mark
from models import Assessment, Mark


@pytest.mark.parametrize("weight", [0, 100])
def test_weight_boundary_values_are_accepted(weight):
    assessment = Assessment(
        id="A1",
        title="Test",
        weight=weight,
        total=20,
    )
    assert assessment.weight == weight


@pytest.mark.parametrize("weight", [-0.01, 100.01])
def test_weight_outside_boundary_is_rejected(weight):
    with pytest.raises(ValidationError):
        Assessment(
            id="A1",
            title="Test",
            weight=weight,
            total=20,
        )


def test_total_weight_of_100_is_allowed():
    from rules import ensure_weight_fits

    ensure_weight_fits([60], 40)


def test_total_weight_above_100_is_rejected():
    from rules import ensure_weight_fits

    with pytest.raises(ValidationError):
        ensure_weight_fits([60], 40.01)



def test_score_boundaries():
    state = {
        "students": {"S1": {"id": "S1", "name": "Ali"}},
        "assessments": {"A1": {"id": "A1", "weight": 10, "total": 20}},
        "marks": [],
    }

    for score in [0, 20]:
        mark = Mark(
            student="S1",
            assessment="A1",
            score=score,
        )

        add_mark(
            state,
            mark,
            lambda: "2026-10-28 10:00:00",
            lambda: None,
        )

    assert len(state["marks"]) == 2



@pytest.mark.parametrize("score", [-0.01, 20.01])
def test_invalid_scores_are_rejected_and_not_stored(score):
    state = {
        "students": {"S1": {"id": "S1", "name": "Ali"}},
        "assessments": {"A1": {"id": "A1", "weight": 10, "total": 20}},
        "marks": [],
    }

    with pytest.raises(ValidationError):
        mark = Mark(
            student="S1",
            assessment="A1",
            score=score,
        )

        add_mark(
            state,
            mark,
            lambda: "2026-10-28 10:00:00",
            lambda: None,
        )

    assert state["marks"] == []


