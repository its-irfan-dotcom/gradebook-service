
from errors import ValidationError


def ensure_weight_fits(existing_weights, new_weight):
    if sum(existing_weights) + new_weight > 100:
        raise ValidationError("Total assessment weight cannot exceed 100")
