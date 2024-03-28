#!/usr/bin/env python3
""" Cache class. In the __init__ method, store an instance of
the Redis client as a private variable named _redis
"""

import redis
import uuid
from functools import wraps
from typing import Callable, List


def call_history(method: Callable) -> Callable:
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        inputs_key = "{}:inputs".format(method.__qualname__)
        outputs_key = "{}:outputs".format(method.__qualname__)

        # Append input arguments to the inputs list
        self._redis.rpush(inputs_key, str(args))

        # Execute the wrapped function to retrieve the output
        output = method(self, *args, **kwargs)

        # Store the output in the outputs list
        self._redis.rpush(outputs_key, output)

        return output

    return wrapper


class Cache:
    def __init__(self) -> None:
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    def store(self, data: str) -> str:
        """ Stores data in redis with randomly generated key """
        key = str(uuid.uuid4())
        client = self._redis
        client.set(key, data)
        return key
