import unittest
from unittest.mock import patch
import io
from web.handlers import VoucherHandler
from base import BaseTestClass
from voucher.models import Voucher, VoucherDB

class TestWeb(BaseTestClass):
    # @unittest.skip("not yet ready")
    # def test_handle_add_voucher(self):
    #     vouch = Voucher(code="leu123", duration="1h")
    #     handler = AddVoucherHandler()
    #
    #     with patch('cli.handlers.voucher.input') as mock_input:
    #         mock_input.side_effect = [vouch.code, "a"] 
    #         handler.handle(self.config)
    #
    #     voucherDB = VoucherDB(self.config)
    #     self.assertEqual(voucherDB.get_voucher(vouch.code), vouch)

    def test_handle_list_voucher(self):
        handler = ListVoucherHandler()

        vouch = Voucher(code="LEU123", duration="1h")
        vouch2 = Voucher(code="LEU456", duration="2h")

        voucherDB = VoucherDB(self.config)
        voucherDB.add_voucher(vouch)
        voucherDB.add_voucher(vouch2)

        with patch('self.wfile', new=io.BufferedIOBase()) as dummy_res:
            handler.handle(self.config)

            output = dummy_res.read().decode()
            self.assertIn(vouch.code, output)
            self.assertIn(vouch2.code, output)

    # @unittest.skip("not yet ready")
    # def test_handle_use_voucher(self):
    #     handler = UseVoucherHandler()
    #
    #     vouch = Voucher(code="LEU123", duration="1h")
    #
    #     voucherDB = VoucherDB(self.config)
    #     voucherDB.add_voucher(vouch)
    #
    #     handler.handle(self.config, vouch.code)
    #
    #     self.assertEqual(voucherDB.get_voucher(vouch.code).used, True)


    # Todo add unhappy testcases


if __name__ == "__main__":
    unittest.main()
