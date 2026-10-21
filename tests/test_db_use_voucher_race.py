"""Tests for the double-spend race fix in DB.use_voucher."""

import pytest


def test_use_voucher_marks_used(config, db):
    db.add_voucher("LEU123", "1h")

    result = db.use_voucher("LEU123")

    assert result.used is True
    assert db.get_voucher("LEU123").used is True


def test_use_voucher_twice_raises(config, db):
    """A second use of the same code must raise, not silently succeed.

    This is the guard that prevents a double spend: the UPDATE only matches
    rows still marked unused, so the second call sees rowcount == 0.
    """
    db.add_voucher("LEU123", "1h")

    db.use_voucher("LEU123")

    with pytest.raises(ValueError):
        db.use_voucher("LEU123")


def test_use_voucher_stays_used_after_failed_retry(config, db):
    db.add_voucher("LEU123", "1h")
    db.use_voucher("LEU123")

    with pytest.raises(ValueError):
        db.use_voucher("LEU123")

    assert db.get_voucher("LEU123").used is True


def test_use_voucher_unknown_code_raises_keyerror(config, db):
    with pytest.raises(KeyError):
        db.use_voucher("LEU000")
