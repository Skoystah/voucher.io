import unittest
from base import BaseTestClass
from voucher.db import AddVoucherParams, GetVoucherParams, GetVoucherRow
from voucher.models import Voucher


class TestDB(BaseTestClass):

    def test_add_voucher(self):

        voucher = Voucher("LEU123", "1h")

        self.db.add_voucher(AddVoucherParams
                              (code= voucher.code,
                               duration= voucher.duration
                               )
                              )

        res = self.db.connection.execute("SELECT * from voucher")
        added_voucher = res.fetchone()
        self.assertEqual((added_voucher["code"], added_voucher["duration"], added_voucher["used"]),
                         (voucher.code, voucher.duration, False))

    
    def test_add_duplicate_voucher_error(self):

        voucher = Voucher("LEU123", "1h")
        params = AddVoucherParams(code= voucher.code, 
                                  duration= voucher.duration
                                  )

        self.db.add_voucher(params)
        
        with self.assertRaises(KeyError):
            self.db.add_voucher(params)

    def test_get_voucher(self):

        voucher = Voucher("LEU123", "1h")
        retrieved_voucher = GetVoucherRow(voucher.code, voucher.duration, False)

        self.db.add_voucher(AddVoucherParams (code= voucher.code, duration= voucher.duration))

        self.assertEqual(self.db.get_voucher(voucher.code), retrieved_voucher)


    def test_get_voucher_non_existing_error(self):

        voucher = Voucher("LEU123", "1h")

        self.db.add_voucher(AddVoucherParams (code= voucher.code, duration= voucher.duration))

        with self.assertRaises(KeyError):
            self.db.get_voucher("LEU666")
            
    def test_use_voucher(self):

        voucher = Voucher("LEU123", "1h")

        self.db.add_voucher(AddVoucherParams (code= voucher.code, duration= voucher.duration))
        self.db.use_voucher(voucher.code)

        self.assertEqual(self.db.get_voucher(voucher.code).used, True)

    def test_get_vouchers_given_duration(self):

        voucher1 = Voucher("LEU123", "1h")
        voucher2 = Voucher("LEU456", "2h")
        voucher3 = Voucher("LEU789", "2h")

        self.db.add_voucher(AddVoucherParams (code= voucher1.code, duration= voucher1.duration))
        self.db.add_voucher(AddVoucherParams (code= voucher2.code, duration= voucher2.duration))
        self.db.add_voucher(AddVoucherParams (code= voucher3.code, duration= voucher3.duration))

        retrieved_voucher2 = GetVoucherRow(voucher2.code, voucher2.duration, False)
        retrieved_voucher3 = GetVoucherRow(voucher3.code, voucher3.duration, False)

        self.assertEqual(self.db.get_vouchers(GetVoucherParams(duration="2h")), 
                         [retrieved_voucher2, retrieved_voucher3])

    def test_get_unused_vouchers(self):

        voucher1 = Voucher("LEU123", "1h")
        voucher2 = Voucher("LEU456", "2h")
        voucher3 = Voucher("LEU789", "2h")

        self.db.add_voucher(AddVoucherParams (code= voucher1.code, duration= voucher1.duration))
        self.db.add_voucher(AddVoucherParams (code= voucher2.code, duration= voucher2.duration))
        self.db.add_voucher(AddVoucherParams (code= voucher3.code, duration= voucher3.duration))

        self.db.use_voucher(voucher2.code)

        retrieved_voucher1 = GetVoucherRow(voucher1.code, voucher1.duration, False)
        retrieved_voucher3 = GetVoucherRow(voucher3.code, voucher3.duration, False)

        self.assertEqual(self.db.get_vouchers(GetVoucherParams(used=False)), 
                         [retrieved_voucher1, retrieved_voucher3])
if __name__ == "__main__":
    unittest.main()

