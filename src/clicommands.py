from typing import Callable, Dict

import repl

class CliCommand():
    def __init__(self, name: str, description: str, callback: Callable[...,None]) -> None:
        self.__name = name
        self.__description = description
        self.__callback = callback

    @property
    def callback(self):
        return self.__callback

def get_commands() -> Dict[str, CliCommand]:
    return {
            "help": CliCommand(
                name= "help",
                description= "show all available commands",
                callback=repl.handle_help
                ),
            "exit": CliCommand(
                name= "exit",
                description= "exit program",
                callback=repl.handle_exit
                ),
            "add": CliCommand(
                name= "add",
                description= "add parking voucher",
                callback=repl.handle_add_voucher
                ),
            "list": CliCommand(
                name= "list",
                description= "list all parking vouchers",
                callback=repl.handle_list_voucher
                ),
            }
            
