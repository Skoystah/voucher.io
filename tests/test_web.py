import unittest
from base import BaseTestClass
from voucher.models import VoucherDB
from voucher.db import Voucher
from web.handlers.voucher import get_vouchers, use_voucher

class TestWeb(BaseTestClass):
    def test_handle_add_voucher(self):
        vouch = Voucher("LEU123", "1h")

        voucherDB = VoucherDB(self.config)
        voucherDB.add_voucher(vouch)

        expected_vouch = Voucher("LEU123", "1h")
        self.assertEqual(voucherDB.get_voucher("LEU123"), expected_vouch)

    def test_handle_list_voucher(self):
        vouch = Voucher(code="LEU123", duration="1h")
        vouch2 = Voucher(code="LEU456", duration="2h")

        voucherDB = VoucherDB(self.config)
        voucherDB.add_voucher(vouch)
        voucherDB.add_voucher(vouch2)

        expected_vouchers = [
                Voucher(code="LEU123", duration="1h"),
                Voucher(code="LEU456", duration="2h")
                ]

        self.assertEqual(get_vouchers(self.config), expected_vouchers)

    def test_handle_use_voucher(self):
        vouch = Voucher(code="LEU123", duration="1h")

        voucherDB = VoucherDB(self.config)
        voucherDB.add_voucher(vouch)

        use_voucher(self.config, "LEU123")

        self.assertEqual(voucherDB.get_voucher("LEU123").used, True)


    # Todo add unhappy testcases


if __name__ == "__main__":
    unittest.main()
