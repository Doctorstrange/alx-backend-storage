#!/usr/bin/env python3
""" Cache class. In the __init__ method, store an instance of
the Redis client as a private variable named _redis
"""

import redis
import uuid
from typing import Union, Callable


class Cache:
    def __init__(self):
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Callable = None) ->
    Union[str, bytes, int, float, None]:
        if not self._redis.exists(key):
            return None
        data = self._redis.get(key)
        if fn:
            return fn(data)
        return data

    def get_str(self, key: str) -> Union[str, None]:
        return self.get(key, fn=lambda d: d.decode("utf-8")
                        if isinstance(d, bytes) else None)

    def get_int(self, key: str) -> Union[int, None]:
        return self.get(key, fn=lambda d: int(d)
                        if isinstance(d, bytes) else None)
