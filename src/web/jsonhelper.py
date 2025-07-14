from typing import Dict, Any
from voucher.models import Voucher

def custom_encode_json(o: Any) -> Dict[str, Any]:
    if isinstance(o, Voucher):
        return {"code": o.code, "duration": o.duration, "used": o.used}
    raise TypeError(f'Cannot deserialize object of {type(o)}')

def custom_decode_json(d: Dict[str, Any]) -> Any:
    if "__voucher__" in d:
        # what if a value is not filled out ?? e.g. used for a new voucher
        return Voucher(d['code'], d['duration'], d['used'])
    return d
