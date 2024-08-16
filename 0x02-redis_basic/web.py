#!/usr/bin/env python3
"""module that has tools for request caching & tracking.
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
        count_key = f'count:{url}'
        result_key = f'result:{url}'

        # Increment the count
        count = redis_store.incr(count_key)

        # Get the cached result
        result = redis_store.get(result_key)
        if result:
            return result.decode('utf-8')

        # Fetch and cache the result
        result = method(url)
        redis_store.setex(result_key, 10, result)

        # Reset the count if it's the first time fetching the result
        if count == 1:
            redis_store.set(count_key, 0)

        return result
    return invoker

@data_cacher
def get_page(url: str) -> str:
    """Returns the content of a URL after caching the request
    """
    return requests.get(url).text
