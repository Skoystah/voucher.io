import cli.repl as repl
import http.server
import sys
from config import Config
from web.handler import create_handler

def run(config: Config, server_class=http.server.HTTPServer):
    server_address = ('', 8000)
    httpd = server_class(server_address, create_handler(config))
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        httpd.server_close()

def main():
    
    config = Config(db="voucher.db")

    args = sys.argv
    print(args)
    if len(args) > 0 and '--cli' in args:
        repl.start(config)
    else:
        run(config)
    

if __name__ == "__main__":
    main()
