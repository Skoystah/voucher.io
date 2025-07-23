from typing import List
import http.server
from http import HTTPStatus
from web.handlers.voucher import get_vouchers, add_voucher, use_voucher
from config import Config
import json
from web.jsonhelper import custom_decode_json, custom_encode_json

def create_handler(config: Config):
    class HTTPVoucherHandler(http.server.BaseHTTPRequestHandler):
        # HTTP METHODS
        def do_GET(self) -> None:
            path = self.extract_path()
            self.log_message(f'GET path {self.path} || {path}')
            match path[0]:
                case "vouchers":
                    self.handle_get_vouchers()
                case default:
                    self.send_error(HTTPStatus.NOT_FOUND, "Not implemented - come back again later")

        def do_POST(self) -> None:
            path = self.extract_path()
            self.log_message(f'POST path {self.path} || {path}')

            match path[0]:
                case "vouchers":
                    self.handle_add_voucher()

        def do_PUT(self) -> None:
            path = self.extract_path()
            self.log_message(f'PUT path {self.path} || {path}')
            
            match path[0]:
                case "vouchers":
                    if len(path) > 1:
                        if path[1]:
                            self.log_message(f'using voucher {path[1]}')
                            self.handle_use_voucher(path[1])
                            return None
                        else:
                            self.send_error(HTTPStatus.BAD_REQUEST, "Missing voucher request data")
                            return None

                    if len(path) > 2:
                        self.send_error(HTTPStatus.NOT_FOUND, "Not implemented - come back again later")
                        return None

                case _:
                    self.send_error(HTTPStatus.NOT_FOUND, "Not implemented - come back again later")

        def do_OPTIONS(self) -> None:
            self.handle_options()

        # HELPER FUNCTIONS
        def extract_path(self) -> List[str]:
            return self.path.strip('/').split('/')

        # HANDLERS
        def handle_get_vouchers(self) -> None:
            try:
                #retrieve vouchers
                vouchers = get_vouchers(config)

                #create response header
                self.send_response(HTTPStatus.OK)
                self.send_header("Content-type", "application/json")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()

                #create response body
                body = json.dumps(vouchers, default=custom_encode_json).encode()
                self.wfile.write(body)
            except Exception as e:
                self.send_error(HTTPStatus.BAD_REQUEST, f"Voucher could not be entered: {e}")

        def handle_add_voucher(self) -> None:
            # Using read() keeps reading forever - read1() reads only whats there(?)
            data = self.rfile.read1()
            para = json.loads(data)
            self.log_message(f"adding voucher {para}")

            try:
                voucher = add_voucher(config, para)
                self.send_response(HTTPStatus.CREATED)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                body = json.dumps(voucher, default=custom_encode_json).encode()
                self.wfile.write(body)
            # Question : should all errors be handled ? Revisit error handling in Python. what if different errors?
            except KeyError as e:
                self.send_error(HTTPStatus.CONFLICT, f"Voucher could not be entered: {e}")

        def handle_use_voucher(self, code: str) -> None:
            self.log_message(f"using voucher with para: {code}")

            try:
                use_voucher(config, code)
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


