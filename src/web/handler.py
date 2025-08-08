import http.server
from http import HTTPStatus
from config import Config
from web.handlers.voucher import get_vouchers, add_voucher, use_voucher
import json
from urllib.parse import urlparse
from web.jsonhelper import custom_encode_json

def create_handler(config: Config):
    class HTTPVoucherHandler(http.server.BaseHTTPRequestHandler):
        # HTTP METHODS
        def do_GET(self) -> None:
            path, query = self.extract_path()
            self.log_message(f'GET path {self.path} || {path} || {query}')
            match path[0]:
                case "vouchers":
                    self.handle_get_vouchers(**query)
                case _:
                    self.send_error(HTTPStatus.NOT_FOUND, "Path does not exist")

        def do_POST(self) -> None:
            path, _ = self.extract_path()
            self.log_message(f'POST path {self.path} || {path}')
            match path[0]:
                case "vouchers":
                    self.handle_add_voucher()

        def do_PUT(self) -> None:
            path, _ = self.extract_path()
            self.log_message(f'PUT path {self.path} || {path}')
            match path[0]:
                case "vouchers":
                    if len(path) > 1:
                        if path[1]:
                            self.log_message(f'using voucher {path[1]}')
                            self.handle_use_voucher(path[1])
                        else:
                            self.send_error(HTTPStatus.BAD_REQUEST, "Missing voucher request data")

                    if len(path) > 2:
                        self.send_error(HTTPStatus.NOT_FOUND, "Path does not exist")
                case _:
                    self.send_error(HTTPStatus.NOT_FOUND, "Path does not exist")

        def do_OPTIONS(self):
            self.handle_options()

        # HELPER FUNCTIONS
        def extract_path(self):
            parsed = urlparse(self.path)
            path = parsed.path.strip('/').split('/')
            query = {}
            for item in parsed.query.split('&'):
                if item:
                    key, value = item.split('=')
                    query[key] = value.lower()

            return path, query

        # HANDLERS
        def handle_get_vouchers(self, **kwargs) -> None:
            try:
                vouchers = get_vouchers(config, **kwargs)

                #create response header
                self.send_response(HTTPStatus.OK)
                self.send_header("Content-type", "application/json")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()

                #create response body
                body = json.dumps(vouchers, default=custom_encode_json).encode()
                self.wfile.write(body)

            except KeyError as e:
                self.send_error(HTTPStatus.BAD_REQUEST, f"Vouchers could not be retrieved: {e}")
            except Exception:
                self.send_error(HTTPStatus.INTERNAL_SERVER_ERROR, "Unexpected Error")

        def handle_add_voucher(self) -> None:
            # Using read() keeps reading forever - read1() reads only whats there(?)
            para = json.loads(self.rfile.read1())
            self.log_message(f"adding voucher {para}")

            try:
                voucher = add_voucher(config, **para)

                ##create response header
                self.send_response(HTTPStatus.CREATED)
                self.send_header("Content-type", "application/json")
                self.end_headers()

                ##create response body
                body = json.dumps(voucher, default=custom_encode_json).encode()
                self.wfile.write(body)
            except KeyError as e:
                self.send_error(HTTPStatus.CONFLICT, f"Voucher could not be entered: {e}")
            except Exception:
                self.send_error(HTTPStatus.INTERNAL_SERVER_ERROR, "Unexpected Error")

        def handle_use_voucher(self, code: str) -> None:
            self.log_message(f"using voucher with para: {code}")

            try:
                use_voucher(config, code)
                
                ##create response header
                self.send_response(HTTPStatus.OK)
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
            except Exception as e:
                self.send_error(HTTPStatus.CONFLICT, f"Voucher could not be updated: {e}")

        # TODO - move this to middleware?
        def handle_options(self) -> None:

            #create response header
            self.send_response(HTTPStatus.NO_CONTENT)
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Access-Control-Allow-Methods", "GET, PUT, POST")
            self.send_header("Access-Control-Allow-Headers", "Content-type")
            self.end_headers()


    return HTTPVoucherHandler


