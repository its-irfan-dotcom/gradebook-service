
import pytest
import gradebook


@pytest.fixture
def state():
    return {
        "students": {
            "S1": {"name": "Ali"}
        },
        "assessments": {
            "A1": {"weight": 10, "total": 20},
            "A2": {"weight": 30, "total": 50},
        },
        "marks": [],
    }


@pytest.fixture
def loaded(monkeypatch, state):
    monkeypatch.setattr(gradebook, "STATE", state)
    return state
