
from rules import ensure_weight_fits


def test_empty_weights_accept_new_weight():
    ensure_weight_fits([], 50)


import pytest

from errors import ValidationError
from rules import ensure_weight_fits


def test_empty_weights_accept_new_weight():
    ensure_weight_fits([], 50)


def test_reject_total_above_100():
    with pytest.raises(ValidationError, match="100"):
        ensure_weight_fits([60], 50)


def test_total_exactly_100_is_allowed():
    ensure_weight_fits([60], 40)


def test_decimal_weights_totaling_100_are_allowed():
    ensure_weight_fits([9.3, 27.3, 33.7], 29.7)
