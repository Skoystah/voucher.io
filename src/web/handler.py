from typing import Any, Dict, List
import http.server
from http import HTTPStatus
from voucher.models import Voucher
from web.handlers.voucher import get_vouchers, add_voucher, use_voucher
from config import Config
import json

def custom_encode_json(o: Any) -> Dict[str, Any]:
    if isinstance(o, Voucher):
        return {'code': o.code, 'duration': o.duration, 'used': o.used}
    raise TypeError(f'Cannot deserialize object of {type(o)}')

def custom_decode_json(d: Dict[str, Any]) -> Any:
    if "__voucher__" in d:
        # what if a value is not filled out ?? e.g. used for a new voucher
        return Voucher(d['code'], d['duration'], d['used'])
    return d


    
def create_handler(config: Config):
    class HTTPVoucherHandler(http.server.BaseHTTPRequestHandler):
        timeout = 2
        def do_GET(self) -> None:
            self.log_message(f'path {self.path}')
            match self.path:
                case "/vouchers":
                    self.handle_get_vouchers()
                case default:
                    self.send_error(HTTPStatus.NOT_FOUND, "Not implemented - come back again later")

        def do_POST(self) -> None:
            match self.path:
                case "/vouchers":
                    self.handle_add_voucher()

        def do_PUT(self) -> None:
            path = self.extract_path()
            self.log_message(f'PUT path {self.path} || {path}')
            
            if len(path) == 0:
                self.send_error(HTTPStatus.NOT_FOUND, "Not implemented - come back again later")
                return None

            match path[0]:
                case "vouchers":
                    if len(path) > 1:
                        if path[1] > ' ':
                            self.log_message(f'using voucher ')
                            self.handle_use_voucher(path[1])
                            return None
                        else:
                            self.send_error(HTTPStatus.NOT_FOUND, "Not implemented - come back again later")
                            return None

                    if len(path) > 2:
                        self.send_error(HTTPStatus.NOT_FOUND, "Not implemented - come back again later")
                        return None

                case default:
                    self.send_error(HTTPStatus.NOT_FOUND, "Not implemented - come back again later")

        def extract_path(self) -> List[str]:
            return self.path.split('/')[1:]

        def handle_get_vouchers(self) -> None:
            try:
                vouchers = get_vouchers(config)
                body = json.dumps(vouchers, default=custom_encode_json).encode()
                self.wfile.write(body)
                self.send_response(HTTPStatus.OK)
                self.send_header("Content-type", "application/json")
                self.end_headers()
            except Exception as e:
                self.send_error(HTTPStatus.BAD_REQUEST, f"Voucher could not be entered: {e}")

        def handle_add_voucher(self) -> None:
            # Using read() keeps reading forever - read1() reads only whats there(?)
            data = self.rfile.read1()
            para = json.loads(data)

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
                self.end_headers()
            except Exception as e:
                self.send_error(HTTPStatus.CONFLICT, f"Voucher could not be updated: {e}")

    return HTTPVoucherHandler


