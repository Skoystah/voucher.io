from config import Config

def handle_help(config: Config, *args):
    #TO-DO - do this flexibly based on the commands - pass to *args?
    print(
"""Available commands:
    add     add a new voucher
    list    show available vouchers
    help    show help
    exit    exit program
"""
)
