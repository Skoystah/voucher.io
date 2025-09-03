import json
import unittest

from web.app import create_app
from base import BaseTestClass
from voucher.models import VoucherDB
from fastapi.testclient import TestClient


class TestHTTP(BaseTestClass):
    def setUp(self) -> None:
        super().setUp()
        self.client = TestClient(create_app(self.config))

    def test_handle_add_voucher(self):
        vouch = {"code": "LEU123", "duration": "1h"}

        expected_vouch = """
        {
            "code": "LEU123",
            "duration": "1h",
            "used": false
        }
        """

        res = self.client.post("/vouchers", json=vouch)
        print(res.json())

        self.assertEqual(res.json(), json.loads(expected_vouch))

    def test_handle_list_voucher(self):
        voucher_codes = [
            "LEU123",
            "LEU456",
        ]
        voucher_durations = [
            "1h",
            "2h",
        ]

        voucherDB = VoucherDB(self.config)

        for code, duration in zip(voucher_codes, voucher_durations):
            voucherDB.add_voucher(code, duration)

        expected_vouchers = """
        [
            {
            "code": "LEU123",
            "duration": "1h",
            "used": false
            },
            {
            "code": "LEU456",
            "duration": "2h",
            "used": false
            }
        ]
        """

        res = self.client.get("/vouchers")

        self.assertEqual(res.json(), json.loads(expected_vouchers))

    def test_handle_list_filtered_voucher_duration(self):
        voucher_codes = [
            "LEU123",
            "LEU456",
        ]
        voucher_durations = [
            "1h",
            "2h",
        ]

        voucherDB = VoucherDB(self.config)

        for code, duration in zip(voucher_codes, voucher_durations):
            voucherDB.add_voucher(code, duration)

        expected_vouchers = """
        [
            {
            "code": "LEU456",
            "duration": "2h",
            "used": false
            }
        ]
        """

        res = self.client.get("/vouchers?duration=2h")

        self.assertEqual(res.json(), json.loads(expected_vouchers))

    def test_handle_list_filtered_voucher_used(self):
        voucher_codes = [
            "LEU123",
            "LEU456",
        ]
        voucher_durations = [
            "1h",
            "2h",
        ]

        voucherDB = VoucherDB(self.config)

        for code, duration in zip(voucher_codes, voucher_durations):
            voucherDB.add_voucher(code, duration)

        expected_vouchers = """
        [
            {
            "code": "LEU456",
            "duration": "2h",
            "used": false
            }
        ]
        """

        voucherDB.use_voucher("LEU123")

        res = self.client.get("/vouchers?includeUsed=false")

        self.assertEqual(res.json(), json.loads(expected_vouchers))

    def test_handle_use_voucher(self):
        voucher_codes = [
            "LEU123",
            "LEU456",
        ]
        voucher_durations = [
            "1h",
            "2h",
        ]

        voucherDB = VoucherDB(self.config)

        for code, duration in zip(voucher_codes, voucher_durations):
            voucherDB.add_voucher(code, duration)

        _ = self.client.put(f"/vouchers/{'LEU123'}")

        self.assertEqual(voucherDB.get_voucher("LEU123").used, True)

    def test_handle_delete_voucher(self):
        voucher_codes = [
            "LEU123",
            "LEU456",
        ]
        voucher_durations = [
            "1h",
            "2h",
        ]

        voucherDB = VoucherDB(self.config)

        for code, duration in zip(voucher_codes, voucher_durations):
            voucherDB.add_voucher(code, duration)

        deleted_voucher = voucher_codes[1]

        _ = self.client.delete(f"http://localhost:8000/vouchers/{deleted_voucher}")

        with self.assertRaises(KeyError):
            voucherDB.get_voucher(deleted_voucher)

    # Todo add unhappy testcases


if __name__ == "__main__":
    unittest.main()
