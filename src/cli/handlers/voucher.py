import cli.handlers.base as base
import voucher.models as voucher

class ListVoucherHandler(base.BaseHandler):

    def handle(self, *args):
        vouchers = self._config.db.get_vouchers()

        if len(vouchers) == 0:
            print("No vouchers available")
            return
        
        print("Available vouchers:\n")
        for voucher in vouchers:
            print(voucher)


class AddVoucherHandler(base.BaseHandler):

    def handle(self, *args):
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

        new_voucher = voucher.Voucher(
                code=code, 
                duration=duration, 
                used=False
                )
        try:
            self._config.db.add_voucher(new_voucher)
            print(f"Added voucher {new_voucher}")
        except Exception as e:
            print(f"Error - {e}")

class UseVoucherHandler(base.BaseHandler):

    def handle(self, *args):
        if len(args) == 0:
            print("Voucher code required")
            return

        code = args[0]

        try:
            self._config.db.use_voucher(code)
        except Exception as e:
            print(f"Error - {e}")

