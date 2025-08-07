import cli.repl as repl
import web.server as server
import sys
from config import Config
from dotenv import load_dotenv
import os
from voucher.db import DB


def main():
    load_dotenv()

    db_url = os.getenv("DATABASE_URL")
    db_auth_token = os.getenv("DATABASE_AUTH_TOKEN")

    if db_url is None:
        raise Exception("DB Url is missing")

    config = Config(db=DB(db_url, db_auth_token, verbose=True))

    args = sys.argv
    print(args)
    if len(args) > 0 and '--cli' in args:
        repl.start(config)
    else:
        server.run(config)
    

if __name__ == "__main__":
    main()
