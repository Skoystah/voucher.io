import repl
import voucher

class Config():
    def __init__(self, db: voucher.VoucherDB) -> None:
        self.__db = db

    @property
    def db(self):
        return self.__db

def main():
    config = Config(voucher.VoucherDB())
    repl.start(config)
         
if __name__ == "__main__":
    main()
