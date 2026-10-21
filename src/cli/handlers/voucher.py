import os

from cli.errors import error_message
from config import Config
from voucher.helper import parse_vouchers_file
from voucher.models import VoucherDB


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
    code = input().strip()
    if not code:
        print("Error - voucher code required")
        return

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
    except KeyError as e:
        print(f"Error - {error_message(e)}")


def handle_add_vouchers_file(config: Config, *args) -> None:
    print("Enter file location/name:")
    file_name = input()

    if not os.path.exists(file_name):
        print(f"File not found: {file_name}")
        return

    voucherDB = VoucherDB(config)

    try:
        vouchers_input = parse_vouchers_file(file_name)
    except ValueError as e:
        print(f"Error - {error_message(e)}")
        return

    added_count = 0
    for code, duration in vouchers_input:
        try:
            new_voucher = voucherDB.add_voucher(code, duration)
            added_count += 1
            print(f"Added voucher {new_voucher}")
        except KeyError as e:
            print(f"Error adding voucher {code}: {error_message(e)}")

    print(f"Successfully added {added_count} vouchers")


def handle_use_voucher(config: Config, *args) -> None:
    if len(args) == 0:
        print("Voucher code required")
        return

    code = args[0]
    voucherDB = VoucherDB(config)

    try:
        used_voucher = voucherDB.use_voucher(code.upper())
        print(f"Used voucher {used_voucher}")
    except (ValueError, KeyError) as e:
        # ValueError: already used. KeyError: never existed.
        print(f"Error - {error_message(e)}")
