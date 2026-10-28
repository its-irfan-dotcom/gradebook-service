from unittest.mock import patch

from hypothesis import given
from hypothesis import strategies as st

import gradebook
from models import Mark


@given(
    scores=st.lists(
        st.integers(min_value=0, max_value=20),
        min_size=1,
        max_size=5,
    )
)
def test_percentage_never_exceeds_weight(scores):
    state = {
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

    for score in scores:
        gradebook.add_mark(
            state,
        Mark(
                student="S1",
                assessment="A1",
                score=score,
            ),
            lambda: "2026-10-28 10:00:00",
            lambda: None,
        )

    with patch.object(gradebook, "STATE", state):
        assert float(gradebook.pct("S1")) <= 10
