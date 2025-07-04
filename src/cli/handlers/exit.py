import sys
import cli.handlers.base as base
import config

class ExitHandler(base.BaseHandler):
    def __init__(self, config: config.Config) -> None:
        super().__init__(config)

    def handle(self, *args):
        print("Exiting application...")
        sys.exit(0)
