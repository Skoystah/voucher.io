import cli.handlers.base as base
from config import Config
from voucher.models import Voucher, VoucherDB

class ListVoucherHandler(base.BaseHandler):

    def handle(self, config: Config, *args):
        voucherDB = VoucherDB(config)

        #todo add arguments
        vouchers = voucherDB.get_vouchers()

        if len(vouchers) == 0:
            print("No vouchers available")
            return
        
        print("Available vouchers:\n")
        for voucher in vouchers:
            print(voucher)


class AddVoucherHandler(base.BaseHandler):

    def handle(self, config: Config, *args):
        print("Add voucher code:")
        code = input()
        #TO-DO - input validation on code

        print(
    """select duration (enter for default 1h):\n
    a) 1h
    b) 2h
    c) 4h
    """
                )
        duration_input = input()
        duration = ""
        match duration_input:
            case "a":
                duration = "1h"
            case "b":
                duration = "2h"
            case "c":
                duration = "4h"
            case default:
                duration = "1h"

        voucherDB = VoucherDB(config)

        new_voucher = Voucher(
                code=code, 
                duration=duration, 
                used=False
                )
        try:
            voucherDB.add_voucher(new_voucher)
            print(f"Added voucher {new_voucher}")
        except Exception as e:
            print(f"Error - {e}")

class UseVoucherHandler(base.BaseHandler):

    def handle(self, config: Config, *args):
        if len(args) == 0:
            print("Voucher code required")
            return

        code = args[0]
        voucherDB = VoucherDB(config)

        try:
            voucherDB.use_voucher(code.upper())
        except Exception as e:
            print(f"Error - {e}")

