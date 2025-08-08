from voucher.models import VoucherDB
from config import Config
import os

def handle_list_vouchers(config: Config, *args) -> None:
    voucherDB = VoucherDB(config)

    #todo add arguments
    vouchers = voucherDB.get_vouchers()

    if len(vouchers) == 0:
        print("No vouchers available")
        return
    
    print("Available vouchers:\n")
    for voucher in vouchers:
        print(voucher)



def handle_add_voucher(config: Config, *args) -> None:
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

    try:
        new_voucher = voucherDB.add_voucher(code,duration)
        print(f"Added voucher {new_voucher}")
    except Exception as e:
        print(f"Error - {e}")

def handle_add_vouchers_bulk(config: Config, *args) -> None:
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
            try:
                new_voucher = voucherDB.add_voucher(code, duration)
                added_count += 1
                print(f"Added voucher {new_voucher}")
            except Exception as e:
                print(f"Error adding voucher {code}: {e}")

    print(f'Successfully added {added_count} vouchers')


def handle_use_voucher(config: Config, *args) -> None:
    if len(args) == 0:
        print("Voucher code required")
        return

    code = args[0]
    voucherDB = VoucherDB(config)

    try:
        voucherDB.use_voucher(code.upper())
    except Exception as e:
        print(f"Error - {e}")

