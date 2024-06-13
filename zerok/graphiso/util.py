import json
from base64 import b64decode, b64encode

def format_dict_payload(s: str, parse_int_keys: bool = True) -> dict:
        d = json.loads(b64decode(s).decode())

        return {int(k): v for k, v in d.items()} if parse_int_keys else d

def pre_format_dict(d: dict) -> str:
    return b64encode(json.dumps(d).encode()).decode()