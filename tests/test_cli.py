import unittest
from unittest.mock import patch
import io
from cli.handlers.exit import handle_exit
from cli.handlers.help import handle_help
from cli.handlers.voucher import handle_list_vouchers, handle_use_voucher, handle_add_voucher
from base import BaseTestClass
from voucher.models import Voucher, VoucherDB

class TestCLI(BaseTestClass):
    def test_handle_help(self):
        with patch('sys.stdout', new=io.StringIO()) as dummy_stdout:
            handle_help(self.config)

            output = dummy_stdout.getvalue().strip()
            #todo take from cli commands?
            self.assertIn("help", output)
            self.assertIn("exit", output)
            self.assertIn("list", output)
            self.assertIn("add", output)

    def test_handle_add_voucher(self):
        vouch = Voucher(code="leu123", duration="1h")

        with patch('cli.handlers.voucher.input') as mock_input:
            mock_input.side_effect = [vouch.code, "a"] 
            handle_add_voucher(self.config)

        voucherDB = VoucherDB(self.config)
        self.assertEqual(voucherDB.get_voucher(vouch.code), vouch)

    def test_handle_list_voucher(self):

        vouch = Voucher(code="LEU123", duration="1h")
        vouch2 = Voucher(code="LEU456", duration="2h")

        voucherDB = VoucherDB(self.config)
        voucherDB.add_voucher(vouch)
        voucherDB.add_voucher(vouch2)

        with patch('sys.stdout', new=io.StringIO()) as dummy_stdout:
            handle_list_vouchers(self.config)

            output = dummy_stdout.getvalue().strip()
            self.assertIn(vouch.code, output)
            self.assertIn(vouch2.code, output)


    def test_handle_use_voucher(self):

        vouch = Voucher(code="LEU123", duration="1h")

        voucherDB = VoucherDB(self.config)
        voucherDB.add_voucher(vouch)

        handle_use_voucher(self.config, vouch.code)

        self.assertEqual(voucherDB.get_voucher(vouch.code).used, True)


    # Todo add unhappy testcases


if __name__ == "__main__":
    unittest.main()
