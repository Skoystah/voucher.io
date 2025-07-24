import sqlite3

class GetVoucherRow():
    def __init__(self, code, duration, used):
        self.code = code
        self.duration = duration
        self.used = used

    def __eq__(self, other):
        return (
                self.code == other.code and
                self.duration == other.duration and
                self.used == other.used
                )

class AddVoucherParams():
    def __init__(self, code, duration):
        self.code = code
        self.duration = duration


class GetVoucherParams():
    def __init__(self, duration = None, used = None):
        self.duration = duration
        self.used = used

class DB():
    def __init__(self, db = "voucher.db"):
        self.connection = sqlite3.connect(db)
        self.connection.row_factory = sqlite3.Row


    def add_voucher(self, voucher):
        data = (voucher.code, voucher.duration)
        try:
            with self.connection:
                self.connection.execute("INSERT INTO voucher (code, duration) VALUES (?, ?)",data)
        except sqlite3.IntegrityError:
            raise KeyError("Voucher already exists")

    def get_voucher(self, code):
        res = self.connection.execute("SELECT * FROM voucher WHERE code = ?", (code,))
        row = res.fetchone()

        if row is None:
            raise KeyError("Voucher does not exist")

        return GetVoucherRow(
            code=row["code"], 
            duration=row["duration"],
            used=False if row["used"] == 0 else True
            )

    def get_vouchers(self, params):
        print("get vouchers", params.used, params.duration)
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

        query += " ORDER BY duration ASC"
        print("get vouchers", params.used, query)

        res = self.connection.execute(query, para)

        for row in res:
            vouchers.append(
                    GetVoucherRow(
                        code=row["code"], 
                        duration=row["duration"],
                        used=False if row["used"] == 0 else True
                        )
                    )
        return vouchers

    def use_voucher(self, code):
        try:
            with self.connection:
                self.connection.execute("UPDATE voucher SET used = 1 WHERE code = ?", (code,))
        except sqlite3.DatabaseError:
            raise ValueError("Voucher not found")




