from pymongo import MongoClient
from pymongo.database import Collection
from pymongo.database import Database


class DB:
    client: MongoClient
    _db: Database
    _db_cache: dict[str, Collection]

    def __init__(self, host: str, port: int, username: str, password: str, db_name: str):
        self.client = MongoClient(host=host, port=port, username=username, password=password)
        self._db = self.client[db_name]
        self._db_cache = {}

    def get_collection(self, collection: str) -> Collection:
        if collection not in self._db_cache:
            self._db_cache[collection] = self._db[collection]
        return self._db_cache[collection]

    def close(self):
        self.client.close()
