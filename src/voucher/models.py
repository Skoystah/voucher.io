from enum import Enum
from typing import List, Optional

from config import Config
from voucher.db import Voucher

class Duration(str, Enum):
    ONE_HOUR = '1h'
    TWO_HOURS = '2h'
    FOUR_HOURS = '4h'
    TWELVE_HOURS = '12h'

class VoucherDB():
    def __init__(self, config: Config):
        self.db = config.db

    def add_voucher(self, 
                    code: str,
                    duration: str) -> Voucher:
        if duration not in Duration:
            raise ValueError('Voucher duration not allowed')

        # TODO validate voucher code length? Not sure whether the length is always the same

        return self.db.add_voucher(code.upper(), duration)


    def get_voucher(self, code: str) -> Voucher:
        return self.db.get_voucher(code)

    def get_vouchers(self, 
                     duration: Optional[str] = None,
                     used: Optional[bool] = None) -> List[Voucher]:
        return self.db.get_vouchers(duration=duration, used=used)

    def use_voucher(self, code: str) -> None:
        self.db.use_voucher(code.upper())   


