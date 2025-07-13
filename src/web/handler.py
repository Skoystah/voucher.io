from typing import Any, Dict
import http.server
from http import HTTPStatus
from voucher.models import Voucher
from web.handlers.voucher import get_vouchers, add_voucher, use_voucher
from config import Config
import json
import logging

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
            path = self.path.split('/')
            self.log_message(f'PUT path {self.path} || {path}')
            
            #path split returns also space before the '/'
            match path[1]:
                case "/vouchers":
                    case 
                    self.log_message(f'using voucher ')
                    self.handle_use_voucher()
                case default:
                    self.send_error(HTTPStatus.NOT_FOUND, "Not implemented - come back again later")

        def handle_get_vouchers(self) -> None:
            self.send_response(HTTPStatus.OK)
            self.send_header("Content-type", "application/json")
            self.end_headers()

            vouchers = get_vouchers(config)
            body = json.dumps(vouchers, default=custom_encode_json).encode()
            self.wfile.write(body)

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
            # Question : should all errors be handled ? Revisit error handling in Python
            except KeyError as e:
                self.send_error(HTTPStatus.CONFLICT, f"Voucher could not be entered: {e}")

        def handle_use_voucher(self) -> None:
            data = self.rfile.read1()
            para = json.loads(data)

            try:
                use_voucher(config, para)
                self.send_response(HTTPStatus.OK)
                self.end_headers()
            except Exception as e:
                self.send_error(HTTPStatus.CONFLICT, f"Voucher could not be updated: {e}")

    return HTTPVoucherHandler


