from typing import List, Dict, Any
from config import Config
from voucher.models import Voucher, VoucherDB


def get_vouchers(config: Config, *args) -> List[Voucher]:
    voucherDB = VoucherDB(config)

    #todo add arguments
    vouchers = voucherDB.get_vouchers()

    if len(vouchers) == 0:
        return []
         
    return vouchers

def add_voucher(config: Config, para: Dict[str, Any]) -> Voucher:
    voucherDB = VoucherDB(config)

    code = para['code']
    duration = para['duration']
    voucher = Voucher(code, duration)
    voucherDB.add_voucher(voucher)

    return voucher
    
def use_voucher(config: Config, code) -> None:
    voucherDB = VoucherDB(config)
    voucherDB.use_voucher(code)


