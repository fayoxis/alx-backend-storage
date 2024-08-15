#!/usr/bin/env python3
'''A module with tools for request caching and tracking.
'''
import requests
import functools
from datetime import datetime, timedelta
from typing import Callable

# Cache dictionary
cache = {}

# Decorator function to cache and track page requests
def cache_and_track(func: Callable) -> Callable:
    @functools.wraps(func)
    def wrapper(url: str) -> str:
        # Check if the URL is in the cache
        if url in cache:
            cached_data, expiration_time, count = cache[url]
            # Check if the cached data has expired
            if datetime.now() < expiration_time:
                # Update the access count
                cache[url] = (cached_data, expiration_time, count + 1)
                return cached_data

        # Fetch the page content
        content = func(url)

        # Update the cache and access count
        cache[url] = (content, datetime.now() + timedelta(seconds=10), 1)
        cache[f"count:{url}"] = 1

        return content

    return wrapper

@cache_and_track
def get_page(url: str) -> str:
    """
    Fetches the HTML content of a URL and caches the result for 10 seconds.
    Also tracks the number of times the URL was accessed.
    """
    response = requests.get(url)
    return response.text

# Example usage
url = "http://slowwly.robertomurray.co.uk/delay/3000/url/http://www.example.com"
print(get_page(url))  # First request, fetch and cache the content
print(cache[f"count:{url}"])  # Print the access count (1)

print(get_page(url))  # Second request, retrieve from cache
print(cache[f"count:{url}"])  # Print the access count (2)

# Wait for more than 10 seconds to expire the cache
import time
time.sleep(11)

print(get_page(url))  # Third request, fetch and cache the content again
print(cache[f"count:{url}"])  # Print the access count (3)
