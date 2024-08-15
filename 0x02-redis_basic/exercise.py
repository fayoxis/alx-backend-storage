#!/usr/bin/env python3
"""
A module that provides a Redis-backed cache implementation.

This module defines a `Cache` class and several helper functions that allow
for the storage and retrieval of data in a Redis data storage. The `Cache`
class provides methods for storing, retrieving, and managing the call history
of operations performed on the cached data.

The helper functions `count_calls` and `call_history` are decorators that
can be used to track the number of calls made to a method and the details of
those calls, respectively. The `replay` function can be used to display the
call history of a method.
"""
import uuid
import redis
from functools import wraps
from typing import Any, Callable, Union


def count_calls(method: Callable) -> Callable:
    """
    A decorator that tracks the number of calls made to a method in a Cache class.

    When the decorated method is called, the decorator increments a counter
    in the Redis data storage, using the method's qualified name as the key.
    The decorated method is then invoked and its return value is returned.

    Args:
        method (Callable): The method to be decorated.

    Returns:
        Callable: The decorated method.
    """
    @wraps(method)
    def invoker(self, *args, **kwargs) -> Any:
        """
        Invokes the given method after incrementing its call counter.
        """
        if isinstance(self._redis, redis.Redis):
            self._redis.incr(method.__qualname__)
        return method(self, *args, **kwargs)
    return invoker


def call_history(method: Callable) -> Callable:
    """
    A decorator that tracks the call details of a method in a Cache class.

    When the decorated method is called, the decorator stores the method's
    inputs and output in the Redis data storage, using the method's qualified
    name as the key prefix. The decorated method is then invoked and its
    return value is returned.

    Args:
        method (Callable): The method to be decorated.

    Returns:
        Callable: The decorated method.
    """
    @wraps(method)
    def invoker(self, *args, **kwargs) -> Any:
        """
        Returns the method's output after storing its inputs and output.
        """
        in_key = '{}:inputs'.format(method.__qualname__)
        out_key = '{}:outputs'.format(method.__qualname__)
        if isinstance(self._redis, redis.Redis):
            self._redis.rpush(in_key, str(args))
        output = method(self, *args, **kwargs)
        if isinstance(self._redis, redis.Redis):
            self._redis.rpush(out_key, output)
        return output
    return invoker


def replay(fn: Callable) -> None:
    """Displays Cache method that retrieves call count and i/o values
    """
    if fn is None or not hasattr(fn, '__self__'):
        return
    redis_store = getattr(fn.__self__, '_redis', None)
    if not isinstance(redis_store, redis.Redis):
        return
    fxn_name = fn.__qualname__
    in_key = '{}:inputs'.format(fxn_name)
    out_key = '{}:outputs'.format(fxn_name)
    fxn_call_count = 0
    if redis_store.exists(fxn_name) != 0:
        fxn_call_count = int(redis_store.get(fxn_name))
    print('{} was called {} times:'.format(fxn_name, fxn_call_count))
    fxn_inputs = redis_store.lrange(in_key, 0, -1)
    fxn_outputs = redis_store.lrange(out_key, 0, -1)
    for fxn_input, fxn_output in zip(fxn_inputs, fxn_outputs):
        print('{}(*{}) -> {}'.format(
            fxn_name,
            fxn_input.decode("utf-8"),
            fxn_output,
        ))


class Cache:
    """
    A class that represents an object for storing data in a Redis data storage.

    This class provides methods for storing, retrieving, and managing the call
    history of operations performed on the cached data. The `store` method
    stores a value in the Redis data storage and returns a unique key. The
    `get` method retrieves a value from the Redis data storage, optionally
    applying a transformation function to the retrieved data. The `get_str`
    and `get_int` methods are convenience wrappers around `get` that
    automatically decode the retrieved value as a string or convert it to an
    integer, respectively.
    """
    def __init__(self) -> None:
        """
        Initializes a Cache instance.

        This method creates a new Redis connection and flushes the database.
        """
        self._redis = redis.Redis()
        self._redis.flushdb(True)

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Stores a value in a Redis data storage and returns the key.

        Args:
            data (Union[str, bytes, int, float]): The data to be stored.

        Returns:
            str: The unique key under which the data is stored.
        """
        data_key = str(uuid.uuid4())
        self._redis.set(data_key, data)
        return data_key

    def get(
            self,
            key: str,
            fn: Callable = None,
            ) -> Union[str, bytes, int, float]:
        """
        Retrieves a value from a Redis data storage.

        Args:
            key (str): The key under which the data is stored.
            fn (Callable, optional): A transformation function to apply to the
                retrieved data.

        Returns:
            Union[str, bytes, int, float]: The retrieved data, optionally
                transformed by the provided function.
        """
        data = self._redis.get(key)
       return fn(data) if fn is not None else data

    def get_str(self, key: str) -> str:
        """
        Retrieves a string value from a Redis data storage.
        """
        return self.get(key, lambda x: x.decode('utf-8'))

    def get_int(self, key: str) -> int:
        """
        Retrieves an integer value from a Redis data storage.
        """
        return self.get(key, lambda x: int(x))
