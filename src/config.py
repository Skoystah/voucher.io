import voucher.models as voucher

class Config():
    def __init__(self, db: voucher.VoucherDB) -> None:
        self.__db = db

    @property
    def db(self):
        return self.__db
