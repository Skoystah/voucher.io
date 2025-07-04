import cli.handlers.base as base
import config
import voucher.voucher as voucher

class ListVoucherHandler(base.BaseHandler):
    def __init__(self, config: config.Config) -> None:
        super().__init__(config)

    def handle(self, *args):
        vouchers = self._config.db.get_vouchers()

        if len(vouchers) == 0:
            print("No vouchers available")
            return
        
        print("Available vouchers:\n")
        for voucher in vouchers:
            print(voucher)


class AddVoucherHandler(base.BaseHandler):
    def __init__(self, config: config.Config) -> None:
        super().__init__(config)

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
        self._config.db.add_voucher(new_voucher)
        print(f"Added voucher {new_voucher}")

