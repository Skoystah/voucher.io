import cli.repl as repl
import web.server as server
import sys
from config import Config


def main():
    config = Config(db="voucher.db")

    args = sys.argv
    print(args)
    if len(args) > 0 and '--cli' in args:
        repl.start(config)
    else:
        server.run(config)
    

if __name__ == "__main__":
    main()
