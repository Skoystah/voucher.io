import unittest
from base import BaseTestClass
from voucher.db import Voucher

from sqlalchemy.orm import Session


class TestDB(BaseTestClass):

    def test_add_voucher(self):
        voucher_code = "LEU123"
        voucher_duration = "1h"
        
        self.db.add_voucher(voucher_code, voucher_duration)

        with Session(self.db.engine) as session:
            expected_voucher = Voucher(voucher_code, voucher_duration, False)
            self.assertEqual(session.get(Voucher, voucher_code) ,expected_voucher)

    
    def test_add_duplicate_voucher_error(self):
        voucher_code = "LEU123"
        voucher_duration = "1h"
        
        self.db.add_voucher(voucher_code, voucher_duration)

        with self.assertRaises(KeyError):
            self.db.add_voucher(voucher_code, voucher_duration)

    def test_get_voucher(self):
        voucher_code = "LEU123"
        voucher_duration = "1h"
        
        self.db.add_voucher(voucher_code, voucher_duration)

        expected_voucher = Voucher(voucher_code, voucher_duration, False)
        self.assertEqual(self.db.get_voucher(expected_voucher.code), expected_voucher)
        print(self.db.get_voucher(voucher_code))

    def test_get_voucher_non_existing_error(self):
        voucher_code = "LEU123"
        other_voucher_code = "LEU666"
        voucher_duration = "1h"
        
        self.db.add_voucher(voucher_code, voucher_duration)

        with self.assertRaises(KeyError):
            self.db.get_voucher(other_voucher_code)

    def test_use_voucher(self):
        voucher_code = "LEU123"
        voucher_duration = "1h"
        
        self.db.add_voucher(voucher_code, voucher_duration)

        self.db.use_voucher(voucher_code)

        self.assertEqual(self.db.get_voucher(voucher_code).used, True)

    def test_use_non_existing_voucher(self):
        voucher_code = "LEU123"
        other_voucher_code = "LEU666"
        voucher_duration = "1h"
        
        self.db.add_voucher(voucher_code, voucher_duration)

        with self.assertRaises(KeyError):
            self.db.use_voucher(other_voucher_code)

    def test_get_vouchers_given_duration(self):

        voucher_codes = [
                "LEU123",
                "LEU456",
                "LEU789"
                ]
        voucher_durations = [
                "1h",
                "2h",
                "2h"
                ]

        for code, duration in zip(voucher_codes, voucher_durations):
            self.db.add_voucher(code, duration)

        expected_duration = "2h"
        expected_vouchers = []
        for code,duration in zip(voucher_codes, voucher_durations):
            if duration == expected_duration:
                expected_vouchers.append(Voucher(code, duration))

        self.assertEqual(self.db.get_vouchers(duration=expected_duration), 
                         expected_vouchers)

    def test_get_unused_vouchers(self):
        voucher_codes = [
                "LEU123",
                "LEU456",
                "LEU789"
                ]
        voucher_durations = [
                "1h",
                "2h",
                "2h"
                ]

        for code, duration in zip(voucher_codes, voucher_durations):
            self.db.add_voucher(code, duration)

        used_code = voucher_codes[1]
        self.db.use_voucher(used_code)

        expected_vouchers = []
        for code,duration in zip(voucher_codes, voucher_durations):
            if code != used_code:
                expected_vouchers.append(Voucher(code, duration))
                
        self.assertEqual(self.db.get_vouchers(used=False), 
                         expected_vouchers)

if __name__ == "__main__":
    unittest.main()

