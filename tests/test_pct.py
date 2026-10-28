
import gradebook


def test_pct_no_marks(monkeypatch):
    # Arrange
    state = {
        "students": {"S1": {"name": "Ali"}},
        "assessments": {},
        "marks": [],
    }
    monkeypatch.setattr(gradebook, "STATE", state)

    # Act
    result = gradebook.pct("S1")

    # Assert
    assert result == "0"


def test_pct_calculates_percentage(monkeypatch):
    state = {
        "students": {"S1": {"name": "Ali"}},
        "assessments": {
            "A1": {"weight": 10, "total": 20}
        },
        "marks": [
            {"student": "S1", "assessment": "A1", "score": 15}
        ],
    }
    monkeypatch.setattr(gradebook, "STATE", state)

    result = gradebook.pct("S1")

    assert result == "7.5"


def test_pct_ignores_unknown_assessment(monkeypatch):
    state = {
        "students": {"S1": {"name": "Ali"}},
        "assessments": {},
        "marks": [
            {"student": "S1", "assessment": "UNKNOWN", "score": 15}
        ],
    }
    monkeypatch.setattr(gradebook, "STATE", state)

    result = gradebook.pct("S1")

    assert result == "0"
