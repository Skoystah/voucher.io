import cli.repl as repl
import web.server as server
import sys
from config import Config
from dotenv import load_dotenv
import os


def main():
    load_dotenv()

    db_url = os.getenv("DATABASE_URL")
    db_auth_token = os.getenv("DATABASE_AUTH_TOKEN")

    config = Config(db_url=db_url, db_auth_token=db_auth_token)

    args = sys.argv
    print(args)
    if len(args) > 0 and '--cli' in args:
        repl.start(config)
    else:
        server.run(config)
    

if __name__ == "__main__":
    main()
