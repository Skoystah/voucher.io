from voucher.db import DB


class Config():
    def __init__(self, db: DB):
        self.db = db

