import unittest
from base import BaseTestClass
from voucher.models import Voucher, VoucherDB
from web.handlers.voucher import get_vouchers, use_voucher

class TestWeb(BaseTestClass):
    def test_handle_add_voucher(self):
        vouch = Voucher(code="leu123", duration="1h")

        voucherDB = VoucherDB(self.config)
        voucherDB.add_voucher(vouch)

        self.assertEqual(voucherDB.get_voucher(vouch.code), vouch)

    def test_handle_list_voucher(self):
        vouch = Voucher(code="LEU123", duration="1h")
        vouch2 = Voucher(code="LEU456", duration="2h")

        voucherDB = VoucherDB(self.config)
        voucherDB.add_voucher(vouch)
        voucherDB.add_voucher(vouch2)

        expected_vouchers = [vouch, vouch2]

        self.assertEqual(get_vouchers(self.config), expected_vouchers)

    def test_handle_use_voucher(self):
        vouch = Voucher(code="LEU123", duration="1h")

        voucherDB = VoucherDB(self.config)
        voucherDB.add_voucher(vouch)

        use_voucher(self.config, vouch.code)

        self.assertEqual(voucherDB.get_voucher(vouch.code).used, True)


    # Todo add unhappy testcases


if __name__ == "__main__":
    unittest.main()
