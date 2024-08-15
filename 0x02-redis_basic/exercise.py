#!/usr/bin/env python3
"""A module to interact with Redis, a NoSQL data storage solution."""
import uuid
import redis
from functools import wraps
from typing import Any, Callable, Union


def count_calls(method: Callable) -> Callable:
    """Decorator to keep track of the number of times a method is called."""
    @wraps(method)
    def wrapper(self, *args, **kwargs) -> Any:
        """Increments the call counter and invokes the decorated method."""
        if isinstance(self._redis, redis.Redis):
            self._redis.incr(method.__qualname__)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    """Decorator to log the inputs and outputs of a method."""
    @wraps(method)
    def wrapper(self, *args, **kwargs) -> Any:
        """Stores inputs, executes the method, and stores the output."""
        in_key = f"{method.__qualname__}:inputs"
        out_key = f"{method.__qualname__}:outputs"
        if isinstance(self._redis, redis.Redis):
            self._redis.rpush(in_key, str(args))
        output = method(self, *args, **kwargs)
        if isinstance(self._redis, redis.Redis):
            self._redis.rpush(out_key, output)
        return output
    return wrapper


def replay(fn: Callable) -> None:
    """Displays the call history of a method, including inputs and outputs."""
    if fn is None or not hasattr(fn, '__self__'):
        return
    instance = getattr(fn, '__self__', None)
    redis_store = getattr(instance, '_redis', None)
    if not isinstance(redis_store, redis.Redis):
        return
    fxn_name = fn.__qualname__
    in_key = f"{fxn_name}:inputs"
    out_key = f"{fxn_name}:outputs"
    fxn_call_count = 0
    if redis_store.exists(fxn_name):
        fxn_call_count = int(redis_store.get(fxn_name))
    print(f"{fxn_name} was called {fxn_call_count} times:")
    fxn_inputs = redis_store.lrange(in_key, 0, -1)
    fxn_outputs = redis_store.lrange(out_key, 0, -1)
    for fxn_input, fxn_output in zip(fxn_inputs, fxn_outputs):
        print(f"{fxn_name}(*{fxn_input.decode('utf-8')}) -> {fxn_output}")


class Cache:
    """Represents a cache backed by Redis for storing and retrieving data."""
    def __init__(self) -> None:
        """Initializes the Redis connection and flushes the database."""
        self._redis = redis.Redis()
        self._redis.flushdb(True)

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Stores data in Redis and returns a unique key for retrieval."""
        data_key = str(uuid.uuid4())
        self._redis.set(data_key, data)
        return data_key

    def get(
            self,
            key: str,
            fn: Callable = None,
            ) -> Union[str, bytes, int, float]:
        """Retrieves data from Redis, optionally applying a transformation."""
        data = self._redis.get(key)
        return fn(data) if fn is not None else data

    def get_str(self, key: str) -> str:
        """Retrieves a string value from Redis."""
        return self.get(key, lambda x: x.decode('utf-8'))

    def get_int(self, key: str) -> int:
        """Retrieves an integer value from Redis."""
        return self.get(key, lambda x: int(x))
