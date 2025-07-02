import unittest
from context import src
from src import voucher

class TestVouchers(unittest.TestCase):
    def test_list_vouchers(self):
        vouch = voucher.Voucher(code="LEU123", duration="1h", used=False)
        vouchers = [vouch]
        voucher_list = voucher.VoucherDB()
        voucher_list.add_voucher(vouch)
        self.assertEqual(vouchers, voucher_list.get_vouchers())


if __name__ == "__main__":
    unittest.main()
