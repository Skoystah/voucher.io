from voucher.db import Voucher

def custom_encode_json(obj):
    if isinstance(obj, Voucher):
        return {"code": obj.code, "duration": obj.duration, "used": obj.used}
    raise TypeError(f'Cannot deserialize object of {type(obj)}')

def custom_decode_json(dct):
    if "__voucher__" in dct:
        # what if a value is not filled out ?? e.g. used for a new voucher
        return Voucher(dct['code'], dct['duration'], dct['used'])
    return dct
