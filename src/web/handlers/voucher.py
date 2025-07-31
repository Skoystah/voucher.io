from voucher.db import Voucher
from voucher.models import VoucherDB


def get_vouchers(config, **kwargs):
    voucherDB = VoucherDB(config)

    vouchers = voucherDB.get_vouchers(**kwargs)

    if len(vouchers) == 0:
        return []
         
    return vouchers

def add_voucher(config, para):
    voucherDB = VoucherDB(config)

    code = para['code']
    duration = para['duration']
    voucher = Voucher(code, duration)
    voucherDB.add_voucher(voucher)

    # TODO - make add_voucher return the voucher, the original voucher was already ditched in the session!
    return Voucher(code,duration, False)
    
def use_voucher(config, code):
    voucherDB = VoucherDB(config)
    voucherDB.use_voucher(code)


