import pytest

from db.models import Voucher
from voucher.models import VoucherDB


def test_add_voucher(config, db):
    voucher_code = "LEU123"
    voucher_duration = "1h"
    voucherDB = VoucherDB(config)

    voucherDB.add_voucher(voucher_code, voucher_duration)

    assert len(db.get_vouchers()) == 1


def test_add_voucher_csv(config, db):
    voucher_code = "LEU123"
    voucher_duration = "1h"
    voucherDB = VoucherDB(config)

    voucherDB.add_voucher(voucher_code, voucher_duration)

    assert len(db.get_vouchers()) == 1


def test_add_voucher_pdf(config, db):
    voucher_code = "LEU123"
    voucher_duration = "1h"
    voucherDB = VoucherDB(config)

    voucherDB.add_voucher(voucher_code, voucher_duration)

    assert len(db.get_vouchers()) == 1


def test_add_existing_voucher_error(config, db):
    voucher_code = "LEU123"
    voucher_duration = "1h"
    voucherDB = VoucherDB(config)

    voucherDB.add_voucher(voucher_code, voucher_duration)

    with pytest.raises(KeyError):
        voucherDB.add_voucher(voucher_code, voucher_duration)

    assert len(db.get_vouchers()) == 1


def test_get_vouchers(config, db):
    voucher_codes = ["LEU123", "LEU456"]
    voucher_durations = ["1h", "2h"]

    voucherDB = VoucherDB(config)

    for code, duration in zip(voucher_codes, voucher_durations):
        db.add_voucher(code, duration)

    expected_vouchers = []
    for code, duration in zip(voucher_codes, voucher_durations):
        expected_vouchers.append(Voucher(code, duration))

    assert voucherDB.get_vouchers() == expected_vouchers


def test_get_vouchers_empty_db(config, db):
    voucherDB = VoucherDB(config)

    assert voucherDB.get_vouchers() == []
    assert len(voucherDB.get_vouchers()) == 0


def test_get_vouchers_filter_unused(config, db):
    voucher_codes = ["LEU123", "LEU456"]
    voucher_durations = ["1h", "2h"]
    voucherDB = VoucherDB(config)

    for code, duration in zip(voucher_codes, voucher_durations):
        db.add_voucher(code, duration)

    used_code = voucher_codes[1]
    voucherDB.use_voucher(used_code)

    expected_vouchers = []
    for code, duration in zip(voucher_codes, voucher_durations):
        if code != used_code:
            expected_vouchers.append(Voucher(code, duration))

    assert voucherDB.get_vouchers(used=False) == expected_vouchers


def test_get_vouchers_filter_duration(config, db):
    voucher_codes = ["LEU123", "LEU456", "LEU789"]
    voucher_durations = ["1h", "2h", "2h"]
    voucherDB = VoucherDB(config)

    for code, duration in zip(voucher_codes, voucher_durations):
        db.add_voucher(code, duration)

    expected_duration = "2h"
    expected_vouchers = []
    for code, duration in zip(voucher_codes, voucher_durations):
        if duration == expected_duration:
            expected_vouchers.append(Voucher(code, duration))

    assert voucherDB.get_vouchers(duration=expected_duration) == expected_vouchers


def test_get_voucher(config, db):
    voucher_code = "LEU123"
    voucher_duration = "1h"
    voucherDB = VoucherDB(config)
    db.add_voucher(voucher_code, voucher_duration)

    expected_voucher = Voucher(voucher_code, voucher_duration, False)
    assert voucherDB.get_voucher(voucher_code) == expected_voucher


def test_get_voucher_not_found_error(config, db):
    voucher_code = "LEU123"
    other_voucher_code = "LEU666"
    voucher_duration = "1h"

    voucherDB = VoucherDB(config)
    db.add_voucher(voucher_code, voucher_duration)

    with pytest.raises(KeyError):
        voucherDB.get_voucher(other_voucher_code)


def test_mark_voucher_as_used(config, db):
    voucher_code = "LEU123"
    voucher_duration = "1h"
    voucherDB = VoucherDB(config)

    db.add_voucher(voucher_code, voucher_duration)

    voucherDB.use_voucher(voucher_code)

    assert db.get_voucher(voucher_code).used is True


def test_delete_voucher(config, db):
    voucher_code = "LEU123"
    voucher_duration = "1h"
    voucherDB = VoucherDB(config)
    db.add_voucher(voucher_code, voucher_duration)

    voucherDB.delete_voucher(voucher_code)

    with pytest.raises(KeyError):
        db.get_voucher(voucher_code)
