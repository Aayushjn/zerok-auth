from collections import defaultdict

_login_cache = defaultdict(dict)


def update_cache(username: str, h: dict[int, list[int]]):
    _login_cache[username]["h"] = h
    if "round" not in _login_cache[username]:
        _login_cache[username]["round"] = 1
    else:
        _login_cache[username]["round"] += 1


def get(username: str) -> dict:
    return _login_cache[username]
