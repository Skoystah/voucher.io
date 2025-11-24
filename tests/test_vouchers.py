import unittest
from base import BaseTestClass
from voucher.models import VoucherDB
from db.models import Voucher


class TestVouchers(BaseTestClass):
    def test_add_voucher(self):
        voucher_code = "LEU123"
        voucher_duration = "1h"
        voucherDB = VoucherDB(self.config)

        voucherDB.add_voucher(voucher_code, voucher_duration)

        self.assertEqual(len(self.db.get_vouchers()), 1)

    def test_add_voucher_csv(self):
        voucher_code = "LEU123"
        voucher_duration = "1h"
        voucherDB = VoucherDB(self.config)

        voucherDB.add_voucher(voucher_code, voucher_duration)

        self.assertEqual(len(self.db.get_vouchers()), 1)

    def test_add_voucher_pdf(self):
        voucher_code = "LEU123"
        voucher_duration = "1h"
        voucherDB = VoucherDB(self.config)

        voucherDB.add_voucher(voucher_code, voucher_duration)

        self.assertEqual(len(self.db.get_vouchers()), 1)

    def test_add_existing_voucher_error(self):
        voucher_code = "LEU123"
        voucher_duration = "1h"
        voucherDB = VoucherDB(self.config)

        voucherDB.add_voucher(voucher_code, voucher_duration)

        with self.assertRaises(KeyError):
            voucherDB.add_voucher(voucher_code, voucher_duration)

        self.assertEqual(len(self.db.get_vouchers()), 1)

    def test_get_vouchers(self):
        voucher_codes = ["LEU123", "LEU456"]
        voucher_durations = ["1h", "2h"]

        voucherDB = VoucherDB(self.config)

        for code, duration in zip(voucher_codes, voucher_durations):
            self.db.add_voucher(code, duration)

        expected_vouchers = []
        for code, duration in zip(voucher_codes, voucher_durations):
            expected_vouchers.append(Voucher(code, duration))

        self.assertEqual(voucherDB.get_vouchers(), expected_vouchers)

    def test_get_vouchers_empty_db(self):
        voucherDB = VoucherDB(self.config)

        self.assertEqual(voucherDB.get_vouchers(), [])
        self.assertEqual(len(voucherDB.get_vouchers()), 0)

    def test_get_vouchers_filter_unused(self):
        voucher_codes = ["LEU123", "LEU456"]
        voucher_durations = ["1h", "2h"]
        voucherDB = VoucherDB(self.config)

        for code, duration in zip(voucher_codes, voucher_durations):
            self.db.add_voucher(code, duration)

        used_code = voucher_codes[1]
        voucherDB.use_voucher(used_code)

        expected_vouchers = []
        for code, duration in zip(voucher_codes, voucher_durations):
            if code != used_code:
                expected_vouchers.append(Voucher(code, duration))

        self.assertEqual(voucherDB.get_vouchers(used=False), expected_vouchers)

    def test_get_vouchers_filter_duration(self):
        voucher_codes = ["LEU123", "LEU456", "LEU789"]
        voucher_durations = ["1h", "2h", "2h"]
        voucherDB = VoucherDB(self.config)

        for code, duration in zip(voucher_codes, voucher_durations):
            self.db.add_voucher(code, duration)

        expected_duration = "2h"
        expected_vouchers = []
        for code, duration in zip(voucher_codes, voucher_durations):
            if duration == expected_duration:
                expected_vouchers.append(Voucher(code, duration))

        self.assertEqual(
            voucherDB.get_vouchers(duration=expected_duration), expected_vouchers
        )

    def test_get_voucher(self):
        voucher_code = "LEU123"
        voucher_duration = "1h"
        voucherDB = VoucherDB(self.config)
        self.db.add_voucher(voucher_code, voucher_duration)

        expected_voucher = Voucher(voucher_code, voucher_duration, False)
        self.assertEqual(voucherDB.get_voucher(voucher_code), expected_voucher)

    def test_get_voucher_not_found_error(self):
        voucher_code = "LEU123"
        other_voucher_code = "LEU666"
        voucher_duration = "1h"

        voucherDB = VoucherDB(self.config)
        self.db.add_voucher(voucher_code, voucher_duration)

        with self.assertRaises(KeyError):
            voucherDB.get_voucher(other_voucher_code)

    def test_mark_voucher_as_used(self):
        voucher_code = "LEU123"
        voucher_duration = "1h"
        voucherDB = VoucherDB(self.config)

        self.db.add_voucher(voucher_code, voucher_duration)

        voucherDB.use_voucher(voucher_code)

        self.assertEqual(self.db.get_voucher(voucher_code).used, True)

    def test_delete_voucher(self):
        voucher_code = "LEU123"
        voucher_duration = "1h"
        voucherDB = VoucherDB(self.config)
        self.db.add_voucher(voucher_code, voucher_duration)

        voucherDB.delete_voucher(voucher_code)

        with self.assertRaises(KeyError):
            self.db.get_voucher(voucher_code)


if __name__ == "__main__":
    unittest.main()
