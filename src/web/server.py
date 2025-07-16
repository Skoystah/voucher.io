import http.server
from config import Config
from web.handler import create_handler

def run(config: Config, server_class=http.server.HTTPServer):
    server_address = ('', 8000)
    httpd = server_class(server_address, create_handler(config))
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        httpd.server_close()
