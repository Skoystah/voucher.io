import unittest
import os
from voucher.helper import parse_vouchers_file


class TestHelper(unittest.TestCase):
    def test_parse_vouchers_file_csv(self):
        vouchers = [
            ("LEU121", "1h"),
            ("LEU122", "2h"),
            ("LEU123", "12h"),
            ("LEU124", "4h"),
            ("LEU125", "1h"),
            ("LEU126", "4h"),
            ("LEU127", "2h"),
            ("LEU128", "1h"),
        ]

        with open("test_handle_add_voucher_bulk.csv", "w") as file:
            for voucher in vouchers:
                file.write(f"{voucher[0]};{voucher[1]}\n")

        self.assertEqual(
            parse_vouchers_file("test_handle_add_voucher_bulk.csv"), vouchers
        )

        os.remove("test_handle_add_voucher_bulk.csv")

    def test_handle_add_vouchers_pdf(self):
        voucher_codes = [
            "LEU2CRPG36K",
            "LEU2CRPGPS3",
            "LEU2CRPGWAH",
            "LEU2CRPGGE9",
            "LEU2CRPGXKW",
            "LEU2CRPGLFU",
            "LEU2CRPG2F2",
            "LEU2CRPGHSL",
            "LEU2CRPGUR5",
            "LEU2CRPGVD3",
        ]
        duration = "2h"

        vouchers = [(code, duration) for code in voucher_codes]

        self.assertEqual(parse_vouchers_file("tests/data/test_vouchers.pdf"), vouchers)


if __name__ == "__main__":
    unittest.main()
