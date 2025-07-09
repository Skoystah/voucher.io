import unittest
from unittest.mock import patch
import io
from cli.handlers.help import HelpHandler
from cli.handlers.voucher import ListVoucherHandler, AddVoucherHandler, UseVoucherHandler
from base import BaseTestClass
from voucher.models import Voucher, VoucherDB

class TestCLI(BaseTestClass):
    def test_handle_help(self):
        handler = HelpHandler()

        with patch('sys.stdout', new=io.StringIO()) as dummy_stdout:
            handler.handle(self.config)

            output = dummy_stdout.getvalue().strip()
            #todo take from cli commands?
            self.assertIn("help", output)
            self.assertIn("exit", output)
            self.assertIn("list", output)
            self.assertIn("add", output)

    def test_handle_add_voucher(self):
        handler = AddVoucherHandler()

        vouch = Voucher(code="LEU123", duration="1h")

    def test_handle_list_voucher(self):
        handler = ListVoucherHandler()

        vouch = Voucher(code="LEU123", duration="1h")
        vouch2 = Voucher(code="LEU456", duration="2h")
        expected_vouchers = [vouch, vouch2]

        self.assertEqual(handler.handle(self.config), expected_vouchers)

if __name__ == "__main__":
    unittest.main()
