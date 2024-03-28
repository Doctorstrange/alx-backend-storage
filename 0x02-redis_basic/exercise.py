#!/usr/bin/env python3
""" Cache class. In the __init__ method, store an instance of
the Redis client as a private variable named _redis
"""

import redis
import uuid
from typing import Union


class Cache:
    """ Cache class
    """
    def __init__(self):
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key
