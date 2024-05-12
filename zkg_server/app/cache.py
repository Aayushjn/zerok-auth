from collections import defaultdict

_login_cache = defaultdict(dict)


def update(username: str, h: dict[int, list[int]], b: int):
    _login_cache[username]["h"] = h
    _login_cache[username]["b"] = b
    if "round" not in _login_cache[username]:
        _login_cache[username]["round"] = 1
    else:
        _login_cache[username]["round"] += 1


def get(username: str) -> dict:
    return _login_cache[username]


def delete(username: str):
    del _login_cache[username]
