from typing import List, Optional
import voucher.db as db

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
    def __init__(self) -> None:
        self.__db = db.DB()

    def add_voucher(self, voucher: Voucher) -> None:
        self.__db.add_voucher(db.AddVoucherParams
                              (code= voucher.code.upper(),
                               duration= voucher.duration
                               )
                              )

    def get_voucher(self, code) -> Voucher:
        row = self.__db.get_voucher(code)
        return Voucher(
                code= row.code,
                duration= row.duration,
                used=row.used
                )

    def get_vouchers(self, used: Optional[bool] = None, duration: Optional[str] = None) -> List[Voucher]:
        vouchers = []
        rows = self.__db.get_vouchers()
        for row in rows:
            vouchers.append(Voucher(
                code= row.code,
                duration= row.duration,
                used=row.used
                )
                            )
        return vouchers

    def use_voucher(self, code) -> None:
        self.__db.use_voucher(code)   


