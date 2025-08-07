from enum import Enum

class Duration(str, Enum):
    ONE_HOUR = '1h'
    TWO_HOURS = '2h'
    FOUR_HOURS = '4h'
    TWELVE_HOURS = '12h'

class VoucherDB():
    def __init__(self, config):
        #TODO - still needed to have this here? Why not take from config directly?
        self.db = config.db

    def add_voucher(self, voucher):
        if voucher.duration not in Duration:
            raise ValueError('Voucher duration not allowed')

        # TODO validate voucher code length? Not sure whether the length is always the same
        voucher.code = voucher.code.upper()
        self.db.add_voucher(voucher)

    def get_voucher(self, code):
        return self.db.get_voucher(code)

    def get_vouchers(self, **kwargs):
        return self.db.get_vouchers(**kwargs)

    def use_voucher(self, code):
        self.db.use_voucher(code.upper())   


