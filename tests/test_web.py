import unittest
from base import BaseTestClass
from voucher.models import VoucherDB
from voucher.db import Voucher
from web.handlers.voucher import get_vouchers, use_voucher

class TestWeb(BaseTestClass):
    def test_handle_add_voucher(self):
        voucher_codes = [
                "LEU123",
                ]
        voucher_durations = [
                "1h",
                ]
        voucherDB = VoucherDB(self.config)

        for code, duration in zip(voucher_codes, voucher_durations):
            voucherDB.add_voucher(code, duration)

        expected_vouch = Voucher("LEU123", "1h")
        self.assertEqual(voucherDB.get_voucher("LEU123"), expected_vouch)

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

        expected_vouchers = [
                Voucher(code="LEU123", duration="1h"),
                Voucher(code="LEU456", duration="2h")
                ]

        self.assertEqual(get_vouchers(self.config, {}), expected_vouchers)

    def test_handle_use_voucher(self):
        voucher_codes = [
                "LEU123",
                ]
        voucher_durations = [
                "1h",
                ]
        voucherDB = VoucherDB(self.config)

        for code, duration in zip(voucher_codes, voucher_durations):
            voucherDB.add_voucher(code, duration)

        use_voucher(self.config, "LEU123")

        self.assertEqual(voucherDB.get_voucher("LEU123").used, True)


    # Todo add unhappy testcases


if __name__ == "__main__":
    unittest.main()
