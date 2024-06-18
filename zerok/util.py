import json
from base64 import b64decode
from base64 import b64encode
from collections import Counter


def format_dict_payload(s: str, parse_int_keys: bool = True) -> dict:
    d = json.loads(b64decode(s).decode())

    return {int(k): v for k, v in d.items()} if parse_int_keys else d


def pre_format_dict(d: dict) -> str:
    return b64encode(json.dumps(d).encode()).decode()


def compare_adj_lists(
    adj_list1: dict[int, list[int]], adj_list2: dict[int, list[int]]
) -> bool:
    def _compare_list(l1: list[int], l2: list[int]) -> bool:
        return Counter(l1) == Counter(l2)

    if len(adj_list1) != len(adj_list2):
        return False

    for v1, v2 in zip(adj_list1.values(), adj_list2.values()):
        if not _compare_list(v1, v2):
            return False

    return True
