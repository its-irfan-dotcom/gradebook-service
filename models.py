
from dataclasses import dataclass


@dataclass(frozen=True)
class Student:
    id: str
    name: str
    joined: str = ""


@dataclass(frozen=True)
class Assessment:
    id: str
    title: str
    weight: float = 0.0
    total: float = 100.0


@dataclass(frozen=True)
class Mark:
    student: str
    assessment: str
    score: float = 0.0
    at: str = ""
