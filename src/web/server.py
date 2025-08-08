from typing import Type
import http.server
from web.handler import create_handler

def run(config, server_class: Type[http.server.HTTPServer] = http.server.HTTPServer):
    server_address = ('', 8000)
    httpd = server_class(server_address, create_handler(config))
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        httpd.server_close()
