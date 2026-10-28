
import json

import pytest

import gradebook


@pytest.fixture
def temporary_data_file(tmp_path, monkeypatch):
    data_file = tmp_path / "data.json"
    monkeypatch.setattr(gradebook, "DATA", data_file)
    return data_file


def test_save_and_load_data(temporary_data_file, monkeypatch):
    # Arrange
    expected = {
        "students": {"S1": {"id": "S1", "name": "Ali"}},
        "assessments": {},
        "marks": [],
    }
    monkeypatch.setattr(gradebook, "STATE", expected)

    # Act
    gradebook.save()
    actual = gradebook.load()

    # Assert
    assert actual == expected


def test_missing_file_returns_empty_data(temporary_data_file):
    # Arrange
    assert not temporary_data_file.exists()

    # Act
    actual = gradebook.load()

    # Assert
    assert actual == {
        "students": {},
        "assessments": {},
        "marks": [],
    }


def test_malformed_json_raises_error(temporary_data_file):
    # Arrange
    temporary_data_file.write_text("{bad", encoding="utf-8")

    # Act and Assert
    with pytest.raises(json.JSONDecodeError):
        gradebook.load()
