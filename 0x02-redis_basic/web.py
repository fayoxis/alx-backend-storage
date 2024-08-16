#!/usr/bin/env python3
"""module that has tools for request caching $ tracking.
"""
import redis
import requests
from functools import wraps
from typing import Callable


redis_store = redis.Redis()
""" module-level instance.
"""


def data_cacher(method: Callable) -> Callable:
    """this is the Caches the output of fetched data.
    """
    @wraps(method)
    def invoker(url) -> str:
        """ wrapper function for caching output.
        """
        redis_store.incr(f'count:{url}')
        result = redis_store.get(f'result:{url}')
        if result:
            return result.decode('utf-8')
        result = method(url)
        redis_store.set(f'count:{url}', 0)
        redis_store.setex(f'result:{url}', 10, result)
        return result
    return invoker


@data_cacher
def get_page(url: str) -> str:
    """Returns the content of a URL after caching the request
    """
    return requests.get(url).text
