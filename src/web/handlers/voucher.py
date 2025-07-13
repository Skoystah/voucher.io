import web.handlers.base as base
from typing import List, Dict, Any
from config import Config
from voucher.models import Voucher, VoucherDB


def get_vouchers(config: Config, *args) -> List[Voucher]:
    voucherDB = VoucherDB(config)

    #todo add arguments
    vouchers = voucherDB.get_vouchers()

    if len(vouchers) == 0:
        return []
         
    return vouchers


def add_voucher(config: Config, para: Dict[str, Any]) -> Voucher:
    voucherDB = VoucherDB(config)

    code = para['code']
    duration = para['duration']
    # print("voucher", code, duration)
    voucher = Voucher(code, duration)
    voucherDB.add_voucher(voucher)

    return voucher
    
def use_voucher(config: Config, para: Dict[str, Any]) -> None:
    voucherDB = VoucherDB(config)

    code = para['code']
    voucherDB.use_voucher(code)

# class AddVoucherHandler(base.BaseHandler):
#
#     def handle(self, config: Config, *args):
#         print("Add voucher code:")
#         code = input()
#         #TO-DO - input validation on code
#
#         print(
#     """select duration (enter for default 1h):\n
#     a) 1h
#     b) 2h
#     c) 4h
#     """
#                 )
#         duration_input = input()
#         duration = ""
#         match duration_input:
#             case "a":
#                 duration = "1h"
#             case "b":
#                 duration = "2h"
#             case "c":
#                 duration = "4h"
#             case default:
#                 duration = "1h"
#
#         voucherDB = VoucherDB(config)
#
#         new_voucher = Voucher(
#                 code=code, 
#                 duration=duration, 
#                 used=False
#                 )
#
# class UseVoucherHandler(base.BaseHandler):
#
#     def handle(self, config: Config, *args):
#         if len(args) == 0:
#             print("Voucher code required")
#             return
#
#         code = args[0]
#         voucherDB = VoucherDB(config)
#
#         try:
#             voucherDB.use_voucher(code.upper())
#         except Exception as e:
#             print(f"Error - {e}")
#
