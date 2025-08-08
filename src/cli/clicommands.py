from typing import Callable
from cli.handlers.exit import handle_exit
from cli.handlers.help import handle_help
from cli.handlers.voucher import handle_list_vouchers, handle_use_voucher, handle_add_voucher, handle_add_vouchers_bulk


class CliCommand():
    def __init__(self, name: str, description: str, handler_function: Callable):
        self.name = name
        self.description = description
        self.handler_function = handler_function


def get_commands():
    return {
            "help": CliCommand(
                name= "help",
                description= "show all available commands",
                handler_function=handle_help
                ),
            "exit": CliCommand(
                name= "exit",
                description= "exit program",
                handler_function=handle_exit
                ),
            "add": CliCommand(
                name= "add",
                description= "add parking voucher",
                handler_function=handle_add_voucher
                ),
            "add-bulk": CliCommand(
                name= "add-bulk",
                description= "add parking vouchers in bulk",
                handler_function=handle_add_vouchers_bulk
                ),
            "list": CliCommand(
                name= "list",
                description= "list all parking vouchers",
                handler_function=handle_list_vouchers
                ),
            "use": CliCommand(
                name= "use",
                description= "use given voucher",
                handler_function=handle_use_voucher
                ),
            }
            
