from typing import List, Optional
from config import Config
import voucher.db as db

class Voucher():
    def __init__(self, code: str, duration: str, used: bool = False) -> None:
        self.code = code.upper()
        self.duration = duration
        self.used = used

    def __eq__(self, other) -> bool:
        return (
                self.code == other.code and
                self.duration == other.duration and
                self.used == other.used
                )

    def __repr__(self) -> str:
        return f'code = {self.code} | duration = {self.duration} | used = {self.used}'

    
class VoucherDB():
    def __init__(self, config: Config) -> None:
        self.db = db.DB(config.db)

    def add_voucher(self, voucher: Voucher) -> None:
        self.db.add_voucher(db.AddVoucherParams
                              (code= voucher.code,
                               duration= voucher.duration
                               )
                              )

    def get_voucher(self, code) -> Voucher:
        row = self.db.get_voucher(code)
        return Voucher(
                code= row.code,
                duration= row.duration,
                used=row.used
                )

    def get_vouchers(self, used: Optional[bool] = None, duration: Optional[str] = None) -> List[Voucher]:
        vouchers = []
        rows = self.db.get_vouchers(
                db.GetVoucherParams(
                    used=used,
                    duration=duration
                    )
                                    )
        for row in rows:
            vouchers.append(Voucher(
                code= row.code,
                duration= row.duration,
                used=row.used
                )
                            )
        return vouchers

    def use_voucher(self, code) -> None:
        self.db.use_voucher(code)   


