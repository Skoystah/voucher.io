import sqlite3
from typing import List, Optional

class GetVoucherRow():
    def __init__(self, code: str, duration: str, used: bool) -> None:
        self.code = code
        self.duration = duration
        self.used = used

    def __eq__(self, other) -> bool:
        return (
                self.code == other.code and
                self.duration == other.duration and
                self.used == other.used
                )

class AddVoucherParams():
    def __init__(self, code: str, duration: str) -> None:
        self.code = code
        self.duration = duration


class GetVoucherParams():
    def __init__(self, duration: Optional[str] = None, used: Optional[bool] = None) -> None:
        self.duration = duration
        self.used = used

class DB():
    def __init__(self, db: str="voucher.db") -> None:
        self.connection = sqlite3.connect(db)
        self.connection.row_factory = sqlite3.Row
        self.cur = self.connection.cursor()


    def add_voucher(self, voucher: AddVoucherParams) -> None:
        data = (voucher.code, voucher.duration)
        try:
            with self.connection:
                self.cur.execute("INSERT INTO voucher (code, duration) VALUES (?, ?)",data)
        except sqlite3.IntegrityError:
            raise KeyError("Voucher already exists")

    def get_voucher(self, code: str) -> GetVoucherRow:
        res = self.cur.execute("SELECT * FROM voucher WHERE code = ?", (code,))
        row = res.fetchone()

        if row is None:
            raise KeyError("Voucher does not exist")

        return GetVoucherRow(
            code=row["code"], 
            duration=row["duration"],
            used=False if row["used"] == 0 else True
            )

    def get_vouchers(self, params: GetVoucherParams) -> List[GetVoucherRow]:
        vouchers = []
        query = "SELECT * FROM voucher"

        args, para = [], []
        if params.duration is not None:
            args.append(" duration = ?")
            para.append(params.duration)
        if params.used is not None:
            args.append(" used = ?")
            para.append(params.used)
        if len(args) > 0:
            query += " WHERE" + " AND".join(args)

        res = self.cur.execute(query, para)

        for row in res:
            vouchers.append(
                    GetVoucherRow(
                        code=row["code"], 
                        duration=row["duration"],
                        used=False if row["used"] == 0 else True
                        )
                    )
        return vouchers

    def use_voucher(self, code: str) -> None:
        try:
            with self.connection:
                self.cur.execute("UPDATE voucher SET used = 1 WHERE code = ?", (code,))
        except sqlite3.DatabaseError:
            raise ValueError("Voucher not found")




