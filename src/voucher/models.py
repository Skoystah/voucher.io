import voucher.db as db

class VoucherDB():
    def __init__(self, config):
        self.db = db.DB(db=config.db, verbose=config.verbose)

    def add_voucher(self, voucher):
        # TODO logic for capitalizing voucher code?
        voucher.code = voucher.code.upper()
        self.db.add_voucher(voucher)

    def get_voucher(self, code):
        return self.db.get_voucher(code)

    def get_vouchers(self, **kwargs):
        return self.db.get_vouchers(**kwargs)

    def use_voucher(self, code):
        self.db.use_voucher(code.upper())   


