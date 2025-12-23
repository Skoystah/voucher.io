import cli.repl as repl
import sys
import os
import uvicorn
from config import Config
from dotenv import load_dotenv
from db.db import DB
from web.app import create_app


def main():
    load_dotenv()

    db_url = os.getenv("DATABASE_URL")
    db_auth_token = os.getenv("DATABASE_AUTH_TOKEN")
    secret_key = os.getenv("SECRET_KEY")
    cert = os.getenv("CERT")
    key_cert = os.getenv("KEY_CERT")

    if secret_key is None:
        raise Exception("Secret key is missing")

    if db_url is None:
        raise Exception("DB Url is missing")

    args = sys.argv

    if len(args) > 0 and "--cli" in args:
        config = Config(
            db=DB(db_url, db_auth_token, verbose=False), secret_key=secret_key
        )
        repl.start(config)
    else:
        config = Config(
            db=DB(db_url, db_auth_token, verbose=True), secret_key=secret_key
        )
        uvicorn.run(
            create_app(config),
            host="0.0.0.0",
            port=8000,
            ssl_keyfile=key_cert,
            ssl_certfile=cert,
        )


if __name__ == "__main__":
    main()
