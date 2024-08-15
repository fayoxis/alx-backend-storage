#!/usr/bin/env python3
"""
A module providing tools for caching and tracking requests.
"""

import requests
from functools import wraps
from typing import Callable
from datetime import datetime, timedelta
from redis import Redis

# Initialize Redis
redis_client = Redis()

def cache_with_expiration(duration: int):
    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            url = args[0]
            cache_key = f"page_content:{url}"
            count_key = f"count:{url}"

            # Check if the page content is cached
            cached_content = redis_client.get(cache_key)
            if cached_content is not None:
                # Increment the access count
                redis_client.incr(count_key)
                return cached_content.decode('utf-8')

            # Fetch the page content
            content = func(*args, **kwargs)

            # Cache the content with expiration
            redis_client.setex(cache_key, duration, content)

            # Initialize the access count
            redis_client.set(count_key, 1)

            return content

        return wrapper
    return decorator

@cache_with_expiration(duration=10)
def get_page(url: str) -> str:
    response = requests.get(url)
    return response.text

# Example usage
print(get_page('http://slowwly.robertomurray.co.uk/delay/3000/url/http://example.org'))
print(get_page('http://slowwly.robertomurray.co.uk/delay/3000/url/http://example.org'))
print(get_page('http://google.com'))
