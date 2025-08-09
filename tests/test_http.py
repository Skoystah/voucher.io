import json
import unittest
import requests
import threading
import http.server
from web.handler import create_handler
from base import BaseTestClass
from voucher.models import VoucherDB

class TestHTTP(BaseTestClass):

    def setUp(self) -> None:
        super().setUp()
        server_address = ('', 8000)
        self.httpd = http.server.HTTPServer(server_address, create_handler(self.config))
        self.thread = threading.Thread(target=self.httpd.serve_forever)
        self.thread.start()

        #time.sleep(0.5)
        
    def tearDown(self) -> None:
        super().tearDown()
        self.httpd.server_close()
        self.httpd.shutdown()
        self.thread.join()

    def test_handle_add_voucher(self):

        vouch = """
        {
            "code": "LEU123",
            "duration": "1h"
        }
        """

        expected_vouch = """
        {
            "code": "LEU123",
            "duration": "1h",
            "used": false
        }
        """

        res = requests.post('http://localhost:8000/vouchers', data=vouch)

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

        res = requests.get('http://localhost:8000/vouchers')
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

        res = requests.get('http://localhost:8000/vouchers?duration=2h')
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

        res = requests.get('http://localhost:8000/vouchers?includeUsed=false')
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


        _ = requests.put(f'http://localhost:8000/vouchers/{"LEU123"}')

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

        _ = requests.delete(f'http://localhost:8000/vouchers/{deleted_voucher}')

        with self.assertRaises(KeyError):
            voucherDB.get_voucher(deleted_voucher)

    # Todo add unhappy testcases


if __name__ == '__main__':
    unittest.main()
