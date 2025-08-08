from typing import List
from config import Config
from voucher.db import Voucher
from voucher.models import VoucherDB


def get_vouchers(config: Config, **kwargs) -> List[Voucher]:

    duration, used = None, None
    for key, value in kwargs.items():
        match key:
            case "includeUsed":
                if value != "true":
                    used = False
            case "duration":
                duration = value
            case _:
                raise KeyError(f'Filter on {key} not possible')
                
    voucherDB = VoucherDB(config)
    vouchers = voucherDB.get_vouchers(duration=duration, used=used)

    if len(vouchers) == 0:
        return []
         
    return vouchers

def add_voucher(config: Config, **kwargs) -> Voucher:

    if 'duration' in kwargs:
        duration = kwargs['duration']
    else:
        raise ValueError('Missing parameter <duration>')

    if 'code' in kwargs:
        code = kwargs['code']
    else:
        raise ValueError('Missing parameter <code>')

    voucherDB = VoucherDB(config)
    added_voucher = voucherDB.add_voucher(code,duration)

    return added_voucher
    
def use_voucher(config: Config, code: str) -> None:

    voucherDB = VoucherDB(config)
    voucherDB.use_voucher(code)


