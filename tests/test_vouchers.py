import unittest
from voucher.models import Voucher, VoucherDB
from voucher.db import DB

class TestVouchers(unittest.TestCase):
    def setUp(self) -> None:
        self.db = DB(":memory:")
        with open("create_db_001","r") as f:
            self.db.cur.executescript(f.read())

    def tearDown(self) -> None:
        self.db.connection.close()

    def test_add_voucher(self):
        vouch = Voucher(code="LEU123", duration="1h", used=False)
        db = VoucherDB(":memory:")

        db.add_voucher(vouch)

        self.assertEqual(len(db.get_vouchers()), 1)

    def test_add_existing_voucher_error(self):
        vouch = Voucher(code="LEU123", duration="1h", used=False)
        db = VoucherDB()
        db.add_voucher(vouch)

        with self.assertRaises(KeyError):
            db.add_voucher(vouch)

        self.assertEqual(len(db.get_vouchers()), 1)

    def test_get_vouchers(self):
        vouch = Voucher(code="LEU123", duration="1h", used=False)
        vouch2 = Voucher(code="LEU456", duration="2h", used=True)
        vouchers = [vouch, vouch2]

        db = VoucherDB()
        db.add_voucher(vouch)
        db.add_voucher(vouch2)

        self.assertEqual(db.get_vouchers(), vouchers) 

    def test_get_vouchers_empty_db(self):
        db = VoucherDB()

        self.assertEqual(db.get_vouchers(), [])
        self.assertEqual(len(db.get_vouchers()), 0)

    def test_get_vouchers_filter_unused(self):
        vouch = Voucher(code="LEU123", duration="1h", used=False)
        vouch2 = Voucher(code="LEU456", duration="2h", used=True)
        vouchers = [vouch]

        db = VoucherDB()
        db.add_voucher(vouch)
        db.add_voucher(vouch2)

        self.assertEqual(db.get_vouchers(used=False), vouchers)

    def test_get_vouchers_filter_duration(self):
        vouch = Voucher(code="LEU123", duration="1h", used=False)
        vouch2 = Voucher(code="LEU456", duration="2h", used=True)
        vouchers = [vouch2]

        db = VoucherDB()
        db.add_voucher(vouch)
        db.add_voucher(vouch2)

        self.assertEqual(db.get_vouchers(duration="2h"), vouchers)

    def test_get_voucher(self):
        vouch = Voucher(code="LEU123", duration="1h", used=False)

        db = VoucherDB()
        db.add_voucher(vouch)

        self.assertEqual(db.get_voucher(vouch.code), vouch)

    def test_get_voucher_not_found_error(self):
        vouch = Voucher(code="LEU123", duration="1h", used=False)
        db = VoucherDB()
        db.add_voucher(vouch)

        with self.assertRaises(KeyError):
            db.get_voucher("LEU666")

    def test_mark_voucher_as_used(self):
        vouch = Voucher(code="LEU123", duration="1h", used=False)
        db = VoucherDB()
        db.add_voucher(vouch)

        db.use_voucher(vouch.code)
        self.assertEqual(db.get_voucher(vouch.code).used, True)
        

if __name__ == "__main__":
    unittest.main()
