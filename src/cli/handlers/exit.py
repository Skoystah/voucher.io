import sys
import cli.handlers.base as base
from config import Config

class ExitHandler(base.BaseHandler):
    def handle(self, config: Config, *args):
        print("Exiting application...")
        sys.exit(0)
