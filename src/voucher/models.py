import voucher.db as db
from enum import Enum

class Duration(str, Enum):
    ONE_HOUR = '1h'
    TWO_HOURS = '2h'
    FOUR_HOURS = '4h'
    TWELVE_HOURS = '12h'

class VoucherDB():
    def __init__(self, config):
        self.db = db.DB(db=config.db, verbose=config.verbose)

    def add_voucher(self, voucher):
        if voucher.duration not in Duration:
            raise ValueError('Voucher duration not allowed')

        # TODO validate voucher code length?

        voucher.code = voucher.code.upper()
        self.db.add_voucher(voucher)

    def get_voucher(self, code):
        return self.db.get_voucher(code)

    def get_vouchers(self, **kwargs):
        return self.db.get_vouchers(**kwargs)

    def use_voucher(self, code):
        self.db.use_voucher(code.upper())   


