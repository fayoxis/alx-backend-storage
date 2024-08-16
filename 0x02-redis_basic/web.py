import requests
from functools import wraps
from typing import Callable
from cachetools import TTLCache

cache = TTLCache(maxsize=100, ttl=10)

def cache_with_count(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(url: str) -> str:
        count_key = f"count:{url}"
        cached_result = cache.get(url)

        if cached_result:
            cache[count_key] = cache.get(count_key, 0) + 1
            return cached_result

        result = func(url)
        cache[url] = result
        cache[count_key] = cache.get(count_key, 0) + 1

        return result

    return wrapper

@cache_with_count
def get_page(url: str) -> str:
    response = requests.get(url)
    return response.text

# Example usage
url = "https://slowwly.robertomurray.co.uk/delay/3000/url/https://www.example.com"
print(get_page(url))
print(f"Count for {url}: {cache[f'count:{url}']}")
