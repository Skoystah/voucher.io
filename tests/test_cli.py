import unittest
from unittest.mock import patch
import io
from cli.handlers.exit import handle_exit
from cli.handlers.help import handle_help
from cli.handlers.voucher import handle_list_vouchers, handle_use_voucher, handle_add_voucher
from base import BaseTestClass
from voucher.models import VoucherDB
from voucher.db import Voucher

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
        vouch = Voucher("LEU123", "1h")

        with patch('cli.handlers.voucher.input') as mock_input:
            mock_input.side_effect = [vouch.code, "a"] 
            handle_add_voucher(self.config)

        voucherDB = VoucherDB(self.config)
        
        expected_vouch = Voucher("LEU123", "1h")
        self.assertEqual(voucherDB.get_voucher(expected_vouch.code), expected_vouch)

    def test_handle_list_voucher(self):

        vouch = Voucher("LEU123", "1h")
        vouch2 = Voucher("LEU456", "2h")

        voucherDB = VoucherDB(self.config)
        voucherDB.add_voucher(vouch)
        voucherDB.add_voucher(vouch2)

        expected_vouch = Voucher("LEU123", "1h")
        expected_vouch2 = Voucher("LEU456", "2h")
        with patch('sys.stdout', new=io.StringIO()) as dummy_stdout:
            handle_list_vouchers(self.config)

            output = dummy_stdout.getvalue().strip()
            self.assertIn(expected_vouch.code, output)
            self.assertIn(expected_vouch2.code, output)


    def test_handle_use_voucher(self):

        vouch = Voucher("LEU123", "1h")

        voucherDB = VoucherDB(self.config)
        voucherDB.add_voucher(vouch)

        handle_use_voucher(self.config, "LEU123")

        self.assertEqual(voucherDB.get_voucher("LEU123").used, True)


    # Todo add unhappy testcases


if __name__ == "__main__":
    unittest.main()
