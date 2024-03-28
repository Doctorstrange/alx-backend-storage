#!/usr/bin/env python3
""" Cache class. In the __init__ method, store an instance of
the Redis client as a private variable named _redis
"""

import redis
import uuid
from functools import wraps
from typing import Any, Callable, Optional, Union


def call_history(method: Callable) -> Callable:
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        key_inputs = "{}:inputs".format(method.__qualname__)
        key_outputs = "{}:outputs".format(method.__qualname__)

        # Append input parameters to Redis list
        self._redis.rpush(key_inputs, str(args))

        # Execute the original method to retrieve the output
        output = method(self, *args, **kwargs)

        # Store the output into Redis list
        self._redis.rpush(key_outputs, str(output))

        return output
    return wrapper


def count_calls(method: Callable) -> Callable:
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper


class Cache:
    def __init__(self) -> None:
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes,  int,  float]) -> str:
        """ Stores data in redis with randomly generated key """
        key = str(uuid.uuid4())
        client = self._redis
        client.set(key, data)
        return key

    def get(self, key: str, fn: Optional[Callable] = None) -> Any:
        """ Gets key's value from redis and converts
            result byte  into correct data type
        """
        client = self._redis
        value = client.get(key)
        if not value:
            return
        if fn is int:
            return self.get_int(value)
        if fn is str:
            return self.get_str(value)
        if callable(fn):
            return fn(value)
        return value

    def get_str(self, data: bytes) -> str:
        """ Converts bytes to string """
        return data.decode('utf-8')

    def get_int(self, data: bytes) -> int:
        """ Converts bytes to integers """
        return int(data)

    def replay(method: Callable) -> None:
        """Replays the call history of a given method,
        formatted as specified."""

        key_inputs = f"{method.__qualname__}:inputs"
        key_outputs = f"{method.__qualname__}:outputs"

        calls_count = method.__self__._redis.get(method.__qualname__)
        if calls_count is None:
            calls_count = 0
        else:
            calls_count = int(calls_count)
        inputs = method.__self__._redis.lrange(key_inputs, 0, -1)
        outputs = method.__self__._redis.lrange(key_outputs, 0, -1)

        print(f"{method.__qualname__} was called {calls_count} times:")
        for input_str, output_str in zip(inputs, outputs):
            inputs_str = repr(ast.literal_eval(input_str))
            print(f"{method.__qualname__}(*{inputs_str}) ->
                    {output_str.decode()}")
