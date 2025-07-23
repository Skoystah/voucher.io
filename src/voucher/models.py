import voucher.db as db

class Voucher():
    def __init__(self, code, duration, used = False):
        self.code = code.upper()
        self.duration = duration
        self.used = used

    def __eq__(self, other):
        return (
                self.code == other.code and
                self.duration == other.duration and
                self.used == other.used
                )

    def __repr__(self):
        return f'code = {self.code} | duration = {self.duration} | used = {self.used}'

    
class VoucherDB():
    def __init__(self, config):
        self.db = db.DB(config.db)

    def add_voucher(self, voucher):
        self.db.add_voucher(db.AddVoucherParams
                              (code= voucher.code,
                               duration= voucher.duration
                               )
                              )

    def get_voucher(self, code):
        row = self.db.get_voucher(code)
        return Voucher(
                code= row.code,
                duration= row.duration,
                used=row.used
                )

    def get_vouchers(self, **kwargs):
        vouchers = []
        used, duration = None, None

        for key, value in kwargs.items():
            match key:
                case "includeUsed":
                    if value == 'true':
                        used = None
                    else:
                        used = False
                case "duration":
                    duration = kwargs["duration"]
                case _:
                    continue

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

    def use_voucher(self, code):
        self.db.use_voucher(code.upper())   


