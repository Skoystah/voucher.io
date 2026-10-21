import io
from unittest.mock import patch

from cli.handlers.help import handle_help
from cli.handlers.voucher import (
    handle_add_voucher,
    handle_add_vouchers_file,
    handle_list_vouchers,
    handle_use_voucher,
)
from db.models import Voucher
from voucher.models import VoucherDB


def test_handle_help(config):
    with patch("sys.stdout", new=io.StringIO()) as dummy_stdout:
        handle_help(config)

        output = dummy_stdout.getvalue().strip()
        # todo take from cli commands?
        assert "help" in output
        assert "exit" in output
        assert "list" in output
        assert "add" in output
        assert "add-file" in output
        assert "add-user" in output


def test_handle_add_voucher(config):
    vouch = Voucher("LEU123", "1h")

    with patch("cli.handlers.voucher.input") as mock_input:
        mock_input.side_effect = [vouch.code, "a"]
        handle_add_voucher(config)

    voucherDB = VoucherDB(config)

    expected_vouch = Voucher("LEU123", "1h")
    assert voucherDB.get_voucher(expected_vouch.code) == expected_vouch


def test_handle_add_vouchers_file_csv(config, tmp_path):
    vouchers = [
        ("LEU121", "1h"),
        ("LEU122", "2h"),
        ("LEU123", "12h"),
        ("LEU124", "4h"),
        ("LEU125", "1h"),
        ("LEU126", "4h"),
        ("LEU127", "2h"),
        ("LEU128", "1h"),
    ]

    csv_file = tmp_path / "test_handle_add_voucher_bulk.csv"
    csv_file.write_text("".join(f"{code};{duration}\n" for code, duration in vouchers))

    with patch("cli.handlers.voucher.input") as mock_input:
        mock_input.side_effect = [str(csv_file)]
        handle_add_vouchers_file(config)

    voucherDB = VoucherDB(config)
    expected_vouchers = [Voucher(code, duration) for code, duration in vouchers]

    assert voucherDB.get_vouchers() == expected_vouchers


# Todo add unhappy testcases


def test_handle_add_vouchers_file_pdf(config):
    voucher_codes = [
        "LEU2CRPG36K",
        "LEU2CRPGPS3",
        "LEU2CRPGWAH",
        "LEU2CRPGGE9",
        "LEU2CRPGXKW",
        "LEU2CRPGLFU",
        "LEU2CRPG2F2",
        "LEU2CRPGHSL",
        "LEU2CRPGUR5",
        "LEU2CRPGVD3",
    ]
    duration = "2h"

    with patch("cli.handlers.voucher.input") as mock_input:
        mock_input.side_effect = ["tests/data/test_vouchers.pdf"]
        handle_add_vouchers_file(config)

    voucherDB = VoucherDB(config)
    expected_vouchers = []
    for code in voucher_codes:
        expected_vouchers.append(Voucher(code, duration))

    assert voucherDB.get_vouchers() == expected_vouchers


def test_handle_list_voucher(config):
    voucher_codes = [
        "LEU123",
        "LEU456",
    ]
    voucher_durations = [
        "1h",
        "2h",
    ]

    voucherDB = VoucherDB(config)

    for code, duration in zip(voucher_codes, voucher_durations):
        voucherDB.add_voucher(code, duration)

    expected_vouch = Voucher("LEU123", "1h")
    expected_vouch2 = Voucher("LEU456", "2h")

    with patch("sys.stdout", new=io.StringIO()) as dummy_stdout:
        handle_list_vouchers(config)

        output = dummy_stdout.getvalue().strip()
        assert expected_vouch.code in output
        assert expected_vouch2.code in output


def test_handle_use_voucher(config):
    voucher_codes = [
        "LEU123",
        "LEU456",
    ]
    voucher_durations = [
        "1h",
        "2h",
    ]

    voucherDB = VoucherDB(config)

    for code, duration in zip(voucher_codes, voucher_durations):
        voucherDB.add_voucher(code, duration)

    handle_use_voucher(config, "LEU123")

    assert voucherDB.get_voucher("LEU123").used is True
