import cli.repl as repl
import sys
import os
import uvicorn
from config import Config
from dotenv import load_dotenv
from voucher.db import DB
from web.app import create_app


def main():
    load_dotenv()

    db_url = os.getenv("DATABASE_URL")
    db_auth_token = os.getenv("DATABASE_AUTH_TOKEN")

    if db_url is None:
        raise Exception("DB Url is missing")

    config = Config(db=DB(db_url, db_auth_token, verbose=True))

    args = sys.argv

    if len(args) > 0 and "--cli" in args:
        repl.start(config)
    else:
        uvicorn.run(create_app(config), host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
