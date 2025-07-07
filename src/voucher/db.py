import sqlite3
from typing import List

class GetVoucherRow():
    def __init__(self, code: str, duration: str, used: bool) -> None:
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
    def used(self):
        return self.__used

class AddVoucherParams():
    def __init__(self, code: str, duration: str) -> None:
        self.__code = code
        self.__duration = duration

    @property
    def code(self):
        return self.__code

    @property
    def duration(self):
        return self.__duration


class GetVoucherParams():
    def __init__(self, code: str, duration: str, used: bool) -> None:
        self.__code = code
        self.__duration = duration
        self.__used = used

class DB():
    def __init__(self) -> None:
        self.__connection = sqlite3.connect("voucher.db")
        self.__connection.row_factory = sqlite3.Row
        self.__cur = self.__connection.cursor()


    def add_voucher(self, voucher: AddVoucherParams) -> None:
        data = (voucher.code, voucher.duration)
        try:
            with self.__connection:
                self.__cur.execute("INSERT INTO voucher (code, duration) VALUES (?, ?)",data)
        except sqlite3.IntegrityError:
            raise KeyError("Voucher already exists")

    def get_voucher(self, code: str) -> GetVoucherRow:
        res = self.__cur.execute("SELECT * FROM voucher WHERE code = ?", (code,))
        row = res.fetchone()
        return GetVoucherRow(
            code=row["code"], 
            duration=row["duration"],
            used=False if row["used"] == 0 else True
            )

    def get_vouchers(self) -> List[GetVoucherRow]:
        vouchers = []
         
        res = self.__cur.execute("SELECT * FROM voucher")
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
            with self.__connection:
                self.__cur.execute("UPDATE voucher SET used = 1 WHERE code = ?", (code,))
        except sqlite3.DatabaseError:
            raise ValueError("Voucher not found")




