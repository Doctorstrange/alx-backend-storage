#!/usr/bin/env python3
""" Cache class. In the __init__ method, store an instance of
the Redis client as a private variable named _redis
"""

import requests
import redis
from functools import wraps
import time


redis_client = redis.Redis()

def cache_with_expiry(seconds):
    """ Decorator for get_page
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            url = args[0]
            cache_back = redis_client.get(url)
            if cache_back:
                return cache_back.decode('utf-8')
            result = func(*args, **kwargs)
            redis_client.setex(url, seconds, result)
            return result
        return wrapper
    return decorator

def track_access_count(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        url = args[0]
        count_key = f"count:{url}"
        redis_client.incr(count_key)
        return func(*args, **kwargs)
    return wrapper

@cache_with_expiry(10)
@track_access_count
def get_page(url: str) -> str:
    response = requests.get(url)
    return response.text
