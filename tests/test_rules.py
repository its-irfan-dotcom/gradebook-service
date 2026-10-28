
from rules import ensure_weight_fits


def test_empty_weights_accept_new_weight():
    ensure_weight_fits([], 50)

