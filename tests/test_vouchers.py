import os
import unittest
from voucher.models import Voucher, VoucherDB
from voucher.db import DB
from config import Config

class TestVouchers(unittest.TestCase):

    def setUp(self) -> None:
        self.config = Config(db="test_voucher.db")
        self.db = DB("test_voucher.db")
        with open("create_db_001","r") as f:
            self.db.cur.executescript(f.read())

    def tearDown(self) -> None:
        self.db.connection.close()
        os.remove("test_voucher.db")
        

    def test_add_voucher(self):
        vouch = Voucher(code="LEU123", duration="1h")
        voucherDB = VoucherDB(self.config)

        voucherDB.add_voucher(vouch)

        self.assertEqual(len(voucherDB.get_vouchers()), 1)

    def test_add_existing_voucher_error(self):
        vouch = Voucher(code="LEU123", duration="1h")
        voucherDB = VoucherDB(self.config)
        voucherDB.add_voucher(vouch)

        with self.assertRaises(KeyError):
            voucherDB.add_voucher(vouch)

        self.assertEqual(len(voucherDB.get_vouchers()), 1)

    def test_get_vouchers(self):
        vouch = Voucher(code="LEU123", duration="1h")
        vouch2 = Voucher(code="LEU456", duration="2h")
        expected_vouchers = [vouch, vouch2]

        voucherDB = VoucherDB(self.config)
        voucherDB.add_voucher(vouch)
        voucherDB.add_voucher(vouch2)

        self.assertEqual(voucherDB.get_vouchers(), expected_vouchers) 

    def test_get_vouchers_empty_db(self):
        voucherDB= VoucherDB(self.config)

        self.assertEqual(voucherDB.get_vouchers(), [])
        self.assertEqual(len(voucherDB.get_vouchers()), 0)

    def test_get_vouchers_filter_unused(self):
        vouch = Voucher(code="LEU123", duration="1h")
        vouch2 = Voucher(code="LEU456", duration="2h")

        voucherDB = VoucherDB(self.config)
        voucherDB.add_voucher(vouch)
        voucherDB.add_voucher(vouch2)

        voucherDB.use_voucher(vouch2.code)
        vouch2.used = True
        expected_vouchers = [vouch]

        self.assertEqual(voucherDB.get_vouchers(used=False), expected_vouchers)

    def test_get_vouchers_filter_duration(self):
        vouch = Voucher(code="LEU123", duration="1h")
        vouch2 = Voucher(code="LEU456", duration="2h")
        expected_vouchers = [vouch2]

        voucherDB = VoucherDB(self.config)
        voucherDB.add_voucher(vouch)
        voucherDB.add_voucher(vouch2)

        self.assertEqual(voucherDB.get_vouchers(duration="2h"), expected_vouchers)

    def test_get_voucher(self):
        vouch = Voucher(code="LEU123", duration="1h")

        voucherDB = VoucherDB(self.config)
        voucherDB.add_voucher(vouch)

        self.assertEqual(voucherDB.get_voucher(vouch.code), vouch)

    def test_get_voucher_not_found_error(self):
        vouch = Voucher(code="LEU123", duration="1h")
        voucherDB = VoucherDB(self.config)
        voucherDB.add_voucher(vouch)

        with self.assertRaises(KeyError):
            voucherDB.get_voucher("LEU666")

    def test_mark_voucher_as_used(self):
        vouch = Voucher(code="LEU123", duration="1h")
        voucherDB = VoucherDB(self.config)
        voucherDB.add_voucher(vouch)

        voucherDB.use_voucher(vouch.code)

        self.assertEqual(voucherDB.get_voucher(vouch.code).used, True)
        

if __name__ == "__main__":
    unittest.main()
