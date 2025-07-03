import unittest
from context import voucher

class TestVouchers(unittest.TestCase):
    def test_add_voucher(self):
        vouch = voucher.Voucher(code="LEU123", duration="1h", used=False)
        db = voucher.VoucherDB()

        db.add_voucher(vouch)

        self.assertEqual(len(db.get_vouchers()), 1)

    def test_add_existing_voucher_error(self):
        vouch = voucher.Voucher(code="LEU123", duration="1h", used=False)
        db = voucher.VoucherDB()
        db.add_voucher(vouch)

        with self.assertRaises(KeyError):
            db.add_voucher(vouch)

        self.assertEqual(len(db.get_vouchers()), 1)

    def test_get_vouchers(self):
        vouch = voucher.Voucher(code="LEU123", duration="1h", used=False)
        vouch2 = voucher.Voucher(code="LEU456", duration="2h", used=True)
        vouchers = [vouch, vouch2]

        db = voucher.VoucherDB()
        db.add_voucher(vouch)
        db.add_voucher(vouch2)

        self.assertEqual(db.get_vouchers(), vouchers) 

    def test_get_vouchers_empty_db(self):
        db = voucher.VoucherDB()

        self.assertEqual(db.get_vouchers(), [])
        self.assertEqual(len(db.get_vouchers()), 0)

    def test_get_vouchers_filter_unused(self):
        vouch = voucher.Voucher(code="LEU123", duration="1h", used=False)
        vouch2 = voucher.Voucher(code="LEU456", duration="2h", used=True)
        vouchers = [vouch]

        db = voucher.VoucherDB()
        db.add_voucher(vouch)
        db.add_voucher(vouch2)

        self.assertEqual(db.get_vouchers(used=False), vouchers)

    def test_get_vouchers_filter_duration(self):
        vouch = voucher.Voucher(code="LEU123", duration="1h", used=False)
        vouch2 = voucher.Voucher(code="LEU456", duration="2h", used=True)
        vouchers = [vouch2]

        db = voucher.VoucherDB()
        db.add_voucher(vouch)
        db.add_voucher(vouch2)

        self.assertEqual(db.get_vouchers(duration="2h"), vouchers)

    def test_get_voucher(self):
        vouch = voucher.Voucher(code="LEU123", duration="1h", used=False)

        db = voucher.VoucherDB()
        db.add_voucher(vouch)

        self.assertEqual(db.get_voucher(vouch.code), vouch)

    def test_get_voucher_not_found_error(self):
        vouch = voucher.Voucher(code="LEU123", duration="1h", used=False)
        db = voucher.VoucherDB()
        db.add_voucher(vouch)

        with self.assertRaises(KeyError):
            db.get_voucher("LEU666")

    def test_mark_voucher_as_used(self):
        vouch = voucher.Voucher(code="LEU123", duration="1h", used=False)
        db = voucher.VoucherDB()
        db.add_voucher(vouch)

        db.use_voucher(vouch.code)
        
        self.assertEqual(db.get_voucher(vouch.code).used, True)
        

if __name__ == "__main__":
    unittest.main()
