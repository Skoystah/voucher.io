from typing import Dict
import config
import cli.handlers.exit as exit
import cli.handlers.help as help
import cli.handlers.voucher as voucher


class CliCommand():
    def __init__(self, name: str, description: str, handler_class: type) -> None:
        self.__name = name
        self.__description = description
        self.__handler_class = handler_class

    def create_handler(self, config: config.Config):
        return self.__handler_class(config)


def get_commands() -> Dict[str, CliCommand]:
    return {
            "help": CliCommand(
                name= "help",
                description= "show all available commands",
                handler_class=help.HelpHandler
                ),
            "exit": CliCommand(
                name= "exit",
                description= "exit program",
                handler_class=exit.ExitHandler
                ),
            "add": CliCommand(
                name= "add",
                description= "add parking voucher",
                handler_class=voucher.AddVoucherHandler
                ),
            "list": CliCommand(
                name= "list",
                description= "list all parking vouchers",
                handler_class=voucher.ListVoucherHandler
                ),
            "use": CliCommand(
                name= "use",
                description= "use parking voucher with given code",
                handler_class=voucher.UseVoucherHandler
                ),
            }
            
