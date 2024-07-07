from collections import defaultdict
from typing import Iterable

_login_cache = defaultdict(dict)


def update(
    username: str,
    batch: int,
    params: list[dict[int, list[int]]],
    challenges: Iterable[int],
):
    _login_cache[username]["batch"] = batch
    _login_cache[username]["params"] = params
    _login_cache[username]["challenges"] = challenges


def get(username: str) -> dict:
    return _login_cache[username]


def delete(username: str):
    del _login_cache[username]
