from typing import List

class Voucher():
    def __init__(self, code: str, duration: str, used: bool = False) -> None:
        self.__code = code
        self.__duration = duration
        self.__used = used

class VoucherDB():
    # needed?
    def __init__(self) -> None:
        self.__vouchers = []

    def add_voucher(self, voucher: Voucher) -> None:
        self.__vouchers.append(voucher)

    def get_vouchers(self) -> List[Voucher]:
        return self.__vouchers


