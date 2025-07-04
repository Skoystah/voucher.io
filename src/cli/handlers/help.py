import cli.handlers.base as base
import config

class HelpHandler(base.BaseHandler):
    def __init__(self, config: config.Config) -> None:
        super().__init__(config)

    def handle(self, *args):
        #TO-DO - do this flexibly based on the commands - pass to *args?
        print(
    """Available commands:
        add     add a new voucher
        list    show available vouchers
        help    show help
        exit    exit program
    """
    )
