
from errors import ValidationError

MAX_TOTAL_WEIGHT: float = 100.0
TOLERANCE: float = 1e-9


def ensure_weight_fits(
    existing_weights: list[float],
    new_weight: float,
) -> None:
    """Raise ValidationError if the total assessment weight exceeds 100."""
    total_weight = sum(existing_weights) + new_weight

    if total_weight > MAX_TOTAL_WEIGHT + TOLERANCE:
        raise ValidationError(
            f"Total assessment weight cannot exceed {MAX_TOTAL_WEIGHT:g}"
        )
