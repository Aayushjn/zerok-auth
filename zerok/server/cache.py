from collections import defaultdict

_login_cache = defaultdict(dict)

def update(username: str, batch_no: int, batch_params: list[ dict[int, list[int]]], batch_challenge: list[int]):
    _login_cache[username]["batch_no"] = batch_no
    _login_cache[username]["batch_params"] = batch_params
    _login_cache[username]["batch_challenge"] = batch_challenge

def get(username: str) -> dict:
    return _login_cache[username]

def delete(username: str):
    del _login_cache[username]