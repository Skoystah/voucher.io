import pytest
from sqlalchemy.orm import Session

from db.models import Voucher


def test_add_voucher(config, db):
    voucher_code = "LEU123"
    voucher_duration = "1h"

    db.add_voucher(voucher_code, voucher_duration)

    with Session(db.engine) as session:
        expected_voucher = Voucher(voucher_code, voucher_duration, False)
        assert session.get(Voucher, voucher_code) == expected_voucher


def test_add_duplicate_voucher_error(config, db):
    voucher_code = "LEU123"
    voucher_duration = "1h"

    db.add_voucher(voucher_code, voucher_duration)

    with pytest.raises(KeyError):
        db.add_voucher(voucher_code, voucher_duration)


def test_get_voucher(config, db):
    voucher_code = "LEU123"
    voucher_duration = "1h"

    db.add_voucher(voucher_code, voucher_duration)

    expected_voucher = Voucher(voucher_code, voucher_duration, False)
    assert db.get_voucher(expected_voucher.code) == expected_voucher


def test_get_voucher_non_existing_error(config, db):
    voucher_code = "LEU123"
    other_voucher_code = "LEU666"
    voucher_duration = "1h"

    db.add_voucher(voucher_code, voucher_duration)

    with pytest.raises(KeyError):
        db.get_voucher(other_voucher_code)


def test_use_voucher(config, db):
    voucher_code = "LEU123"
    voucher_duration = "1h"

    db.add_voucher(voucher_code, voucher_duration)

    db.use_voucher(voucher_code)

    assert db.get_voucher(voucher_code).used is True


def test_use_non_existing_voucher(config, db):
    voucher_code = "LEU123"
    other_voucher_code = "LEU666"
    voucher_duration = "1h"

    db.add_voucher(voucher_code, voucher_duration)

    with pytest.raises(KeyError):
        db.use_voucher(other_voucher_code)


def test_get_vouchers_given_duration(config, db):
    voucher_codes = ["LEU123", "LEU456", "LEU789"]
    voucher_durations = ["1h", "2h", "2h"]

    for code, duration in zip(voucher_codes, voucher_durations):
        db.add_voucher(code, duration)

    expected_duration = "2h"
    expected_vouchers = []
    for code, duration in zip(voucher_codes, voucher_durations):
        if duration == expected_duration:
            expected_vouchers.append(Voucher(code, duration))

    assert db.get_vouchers(duration=expected_duration) == expected_vouchers


def test_get_unused_vouchers(config, db):
    voucher_codes = ["LEU123", "LEU456", "LEU789"]
    voucher_durations = ["1h", "2h", "2h"]

    for code, duration in zip(voucher_codes, voucher_durations):
        db.add_voucher(code, duration)

    used_code = voucher_codes[1]
    db.use_voucher(used_code)

    expected_vouchers = []
    for code, duration in zip(voucher_codes, voucher_durations):
        if code != used_code:
            expected_vouchers.append(Voucher(code, duration))

    assert db.get_vouchers(used=False) == expected_vouchers


def test_delete_voucher(config, db):
    voucher_codes = ["LEU123", "LEU456", "LEU789"]
    voucher_durations = ["1h", "2h", "2h"]

    for code, duration in zip(voucher_codes, voucher_durations):
        db.add_voucher(code, duration)

    deleted_code = voucher_codes[1]
    db.delete_voucher(deleted_code)

    with pytest.raises(KeyError):
        db.get_voucher(deleted_code)
