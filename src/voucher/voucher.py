from typing import List, Optional

class Voucher():
    def __init__(self, code: str, duration: str, used: bool = False) -> None:
        self.__code = code
        self.__duration = duration
        self.__used = used

    @property
    def code(self):
        return self.__code

    @property
    def duration(self):
        return self.__duration
    
    @property
    def used(self) -> bool:
        return self.__used

    @used.setter
    def used(self, used):
        self.__used = used

    def __repr__(self) -> str:
        return f'code = {self.__code} | duration = {self.__duration} | used = {self.__used}'
    
class VoucherDB():
    # needed?
    def __init__(self) -> None:
        self.__vouchers = {}

    def add_voucher(self, voucher: Voucher) -> None:
        if voucher.code in self.__vouchers:
            raise KeyError('Voucher already exists')

        self.__vouchers[voucher.code] = voucher

    def get_voucher(self, code) -> Voucher:
        if code in self.__vouchers:
            return self.__vouchers[code]
        
        raise KeyError('Voucher not found')

    def get_vouchers(self, used: Optional[bool] = None, duration: Optional[str] = None) -> List[Voucher]:
        vouchers = []

        for voucher in self.__vouchers.values():
            if used is not None and used != voucher.used:
                continue

            if duration is not None and duration != voucher.duration:
                continue

            vouchers.append(voucher)

        return vouchers

    def use_voucher(self, code) -> None:
        if code in self.__vouchers:
            self.__vouchers[code].used = True
            return
        
        raise ValueError('Voucher not found')


