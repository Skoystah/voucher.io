import json
import unittest
import requests
import threading
import http.server
from web.handler import create_handler
from base import BaseTestClass
from voucher.models import VoucherDB
from voucher.db import Voucher

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

        vouch = Voucher(code='LEU123', duration='1h')
        vouch2 = Voucher(code='LEU456', duration='2h')

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

        voucherDB = VoucherDB(self.config)
        voucherDB.add_voucher(vouch)
        voucherDB.add_voucher(vouch2)

        res = requests.get('http://localhost:8000/vouchers')
        self.assertEqual(res.json(), json.loads(expected_vouchers))

    def test_handle_list_filtered_voucher_duration(self):

        vouch = Voucher(code='LEU123', duration='1h')
        vouch2 = Voucher(code='LEU456', duration='2h')

        expected_vouchers = """
        [
            {
            "code": "LEU456",
            "duration": "2h",
            "used": false
            }
        ]
        """

        voucherDB = VoucherDB(self.config)
        voucherDB.add_voucher(vouch)
        voucherDB.add_voucher(vouch2)

        res = requests.get('http://localhost:8000/vouchers?duration=2h')
        self.assertEqual(res.json(), json.loads(expected_vouchers))

    def test_handle_list_filtered_voucher_used(self):

        vouch = Voucher(code='LEU123', duration='1h')
        vouch2 = Voucher(code='LEU456', duration='2h')

        expected_vouchers = """
        [
            {
            "code": "LEU456",
            "duration": "2h",
            "used": false
            }
        ]
        """

        voucherDB = VoucherDB(self.config)
        voucherDB.add_voucher(vouch)
        voucherDB.add_voucher(vouch2)
        voucherDB.use_voucher("LEU123")

        res = requests.get('http://localhost:8000/vouchers?includeUsed=false')
        self.assertEqual(res.json(), json.loads(expected_vouchers))

    def test_handle_use_voucher(self):
        vouch = Voucher(code='LEU123', duration='1h')

        voucherDB = VoucherDB(self.config)
        voucherDB.add_voucher(vouch)

        _ = requests.put(f'http://localhost:8000/vouchers/{"LEU123"}')

        self.assertEqual(voucherDB.get_voucher("LEU123").used, True)


    # Todo add unhappy testcases


if __name__ == '__main__':
    unittest.main()
