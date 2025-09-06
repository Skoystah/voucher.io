from voucher.models import VoucherDB
from voucher.helper import parse_vouchers_file
from config import Config
import os
import re
from pypdf import PdfReader


def handle_list_vouchers(config: Config, *args) -> None:
    voucherDB = VoucherDB(config)

    # todo add arguments
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
    # TO-DO - input validation on code

    print(
        """select duration (enter for default 1h):\n
1) 1h
2) 2h
3) 4h
4) 12h
"""
    )
    duration_input = input()
    duration = ""
    match duration_input:
        case "1":
            duration = "1h"
        case "2":
            duration = "2h"
        case "3":
            duration = "4h"
        case "4":
            duration = "12h"
        case _:
            duration = "1h"

    voucherDB = VoucherDB(config)

    try:
        new_voucher = voucherDB.add_voucher(code, duration)
        print(f"Added voucher {new_voucher}")
    except Exception as e:
        print(f"Error - {e}")


def handle_add_vouchers_file(config: Config, *args) -> None:
    print("Enter file location/name:")
    file_name = input()

    if not os.path.exists(file_name):
        print("File name required")
        return

    added_count = 0
    voucherDB = VoucherDB(config)
    vouchers_input = parse_vouchers_file(file_name)

    for code, duration in vouchers_input:
        try:
            new_voucher = voucherDB.add_voucher(code, duration)
            added_count += 1
            print(f"Added voucher {new_voucher}")
        except Exception as e:
            print(f"Error adding voucher {code}: {e}")

    print(f"Successfully added {added_count} vouchers")


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


def convert_duration_text(text: str) -> str:
    match text:
        case "1 uur":
            return "1h"
        case "2 uur":
            return "2h"
        case "4 uur":
            return "4h"
        case "12 uur":
            return "12h"
        case _:
            raise ValueError(f"Duration {text} does not exists")
