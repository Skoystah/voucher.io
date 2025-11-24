import unittest
from unittest.mock import patch
import os
import io
from cli.handlers.help import handle_help
from cli.handlers.voucher import (
    handle_list_vouchers,
    handle_use_voucher,
    handle_add_voucher,
    handle_add_vouchers_file,
)
from base import BaseTestClass
from voucher.models import VoucherDB
from db.models import Voucher


class TestCLI(BaseTestClass):
    def test_handle_help(self):
        with patch("sys.stdout", new=io.StringIO()) as dummy_stdout:
            handle_help(self.config)

            output = dummy_stdout.getvalue().strip()
            # todo take from cli commands?
            self.assertIn("help", output)
            self.assertIn("exit", output)
            self.assertIn("list", output)
            self.assertIn("add", output)
            self.assertIn("add-file", output)
            self.assertIn("add-user", output)

    def test_handle_add_voucher(self):
        vouch = Voucher("LEU123", "1h")

        with patch("cli.handlers.voucher.input") as mock_input:
            mock_input.side_effect = [vouch.code, "a"]
            handle_add_voucher(self.config)

        voucherDB = VoucherDB(self.config)

        expected_vouch = Voucher("LEU123", "1h")
        self.assertEqual(voucherDB.get_voucher(expected_vouch.code), expected_vouch)

    def test_handle_add_vouchers_file_csv(self):
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

        with open("test_handle_add_voucher_bulk.csv", "w") as file:
            for voucher in vouchers:
                file.write(f"{voucher[0]};{voucher[1]}\n")

        with patch("cli.handlers.voucher.input") as mock_input:
            mock_input.side_effect = ["test_handle_add_voucher_bulk.csv"]
            handle_add_vouchers_file(self.config)

        voucherDB = VoucherDB(self.config)
        expected_vouchers = []
        for code, duration in vouchers:
            expected_vouchers.append(Voucher(code, duration))

        self.assertEqual(voucherDB.get_vouchers(), expected_vouchers)

        os.remove("test_handle_add_voucher_bulk.csv")

    # Todo add unhappy testcases

    def test_handle_add_vouchers_file_pdf(self):
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
            handle_add_vouchers_file(self.config)

        voucherDB = VoucherDB(self.config)
        expected_vouchers = []
        for code in voucher_codes:
            expected_vouchers.append(Voucher(code, duration))

        self.assertEqual(voucherDB.get_vouchers(), expected_vouchers)

    def test_handle_list_voucher(self):
        voucher_codes = [
            "LEU123",
            "LEU456",
        ]
        voucher_durations = [
            "1h",
            "2h",
        ]

        voucherDB = VoucherDB(self.config)

        for code, duration in zip(voucher_codes, voucher_durations):
            voucherDB.add_voucher(code, duration)

        expected_vouch = Voucher("LEU123", "1h")
        expected_vouch2 = Voucher("LEU456", "2h")

        with patch("sys.stdout", new=io.StringIO()) as dummy_stdout:
            handle_list_vouchers(self.config)

            output = dummy_stdout.getvalue().strip()
            self.assertIn(expected_vouch.code, output)
            self.assertIn(expected_vouch2.code, output)

    def test_handle_use_voucher(self):
        voucher_codes = [
            "LEU123",
            "LEU456",
        ]
        voucher_durations = [
            "1h",
            "2h",
        ]

        voucherDB = VoucherDB(self.config)

        for code, duration in zip(voucher_codes, voucher_durations):
            voucherDB.add_voucher(code, duration)

        handle_use_voucher(self.config, "LEU123")

        self.assertEqual(voucherDB.get_voucher("LEU123").used, True)


if __name__ == "__main__":
    unittest.main()
