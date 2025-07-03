import voucher
import clicommands
import sys
import main


def handle_help(config: main.Config):
    print(
            """Available commands:
                add     add a new voucher
                list    show available vouchers
                help    show help
                exit    exit program
            """
            )
    
def handle_exit(config: main.Config):
    print("Exiting application...")
    sys.exit(0)

def handle_list_voucher(config: main.Config):
    vouchers = config.db.get_vouchers()

    if len(vouchers) == 0:
        print("No vouchers available")
        return
    
    print("Available vouchers:\n")
    for voucher in vouchers:
        print(voucher)

def handle_add_voucher(config: main.Config):

    print("add voucher code:")
    code = input()
    print(
            """select duration:\n
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
    config.db.add_voucher(new_voucher)
    print(f"Added voucher {new_voucher}")

def start(config: main.Config):

    commands = clicommands.get_commands()

    print("Choose action:")

    while True:
        print(">", end=" ")
        ipt = input().split(" ")

        command = ipt[0]
        args = []
        if len(ipt) > 1:
            args = ipt[1:]

        if command in commands:
            handler = commands[command].callback
            handler(config, *args)
        else:
            print("command unknown")
        continue

