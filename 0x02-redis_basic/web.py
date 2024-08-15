#!/usr/bin/env python3
"""
A module providing tools for caching and tracking requests.
"""
import redis
import requests
from functools import wraps
from typing import Callable


# The module-level Redis instance for caching and tracking
redis_store = redis.Redis()


def data_cacher(method: Callable) -> Callable:
    """
    A decorator function that caches the output of the decorated function.
    It uses Redis to store the cached data and track the number of requests.
    """
    @wraps(method)
    def wrapper(url) -> str:
        """
        The wrapper function that implements the caching logic.
        It increments the request count, checks if the result is cached,
        and if not, calls the decorated function and caches the result.
        """
        # Increment the request count for the given URL
        redis_store.incr(f'count:{url}')
        
        # Check if the result is cached
        result = redis_store.get(f'result:{url}')
        if result:
            return result.decode('utf-8')
        
        # If not cached, call the decorated function and cache the result
        result = method(url)
        redis_store.set(f'count:{url}', 0)
        redis_store.setex(f'result:{url}', 10, result)
        return result
    return wrapper


@data_cacher
def get_page(url: str) -> str:
    """
    A function that fetches the content of a URL.
    It is decorated with the data_cacher decorator to cache the response
    and track the number of requests for the given URL.
    """
    return requests.get(url).text
