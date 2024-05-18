from hashlib import blake2b
from hashlib import sha3_512

HASHERS = {
    "sha3_512": lambda x: sha3_512(x).digest(),
    "blake2b": lambda x: blake2b(x).digest(),
}


def hash_and_encode_data(data: bytes | str, hash_algo: str = "sha3_512") -> bytes:
    """
    Hashes the given data using the specified hash algorithm. The hash algorithm must generate at least 512 bits of
    output.
    """
    if hash_algo not in HASHERS:
        raise ValueError(f"{hash_algo} not supported")

    if isinstance(data, str):
        data = data.encode()
    hashed = HASHERS[hash_algo](data)
    return hashed
