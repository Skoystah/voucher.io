from voucher.models import VoucherDB
from voucher.db import Voucher
import os

def handle_list_vouchers(config, *args):
    voucherDB = VoucherDB(config)

    #todo add arguments
    vouchers = voucherDB.get_vouchers()

    if len(vouchers) == 0:
        print("No vouchers available")
        return
    
    print("Available vouchers:\n")
    for voucher in vouchers:
        print(voucher)



def handle_add_voucher(config, *args):
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
        case _:
            duration = "1h"

    voucherDB = VoucherDB(config)
    new_voucher = Voucher(code,duration) 

    try:
        voucherDB.add_voucher(new_voucher)
        print(f"Added voucher {new_voucher}")
    except Exception as e:
        print(f"Error - {e}")

def handle_add_vouchers_bulk(config, *args) -> None:
    if len(args) == 0:
        print("File name required")
        return

    file_name = args[0]
    if not os.path.exists(file_name):
        print("File does not exist")
        return

    added_count = 0

    voucherDB = VoucherDB(config)

    with open(file_name, 'r') as f:
        for line in f:
            code, duration = line.strip().split(';')
            # print(code, duration)
            try:
                voucherDB.add_voucher(Voucher(code, duration))
                added_count += 1
                print(f"Added voucher {code} with duration {duration}")
            except Exception as e:
                print(f"Error adding voucher {code}: {e}")

    print(f'Successfully added {added_count} vouchers')


def handle_use_voucher(config, *args) -> None:
    if len(args) == 0:
        print("Voucher code required")
        return

    code = args[0]
    voucherDB = VoucherDB(config)

    try:
        voucherDB.use_voucher(code.upper())
    except Exception as e:
        print(f"Error - {e}")

