#!/usr/bin/env python3
"""A module that provides a Redis-backed cache implementation.

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
    """decorator that tracks n of calls made to a method in a Cache class.
    """
    @wraps(method)
    def invoker(self, *args, **kwargs) -> Any:
        """Invokes the given method after incrementing its call counter.
        When the decorated method called decorator stores the method's
        inputs and output in the Redis data storage,
        """
        redis_instance = self._redis
        while isinstance(redis_instance, redis.Redis):
            redis_instance.incr(method.__qualname__)
            break
        return method(self, *args, **kwargs)
    return invoker


def call_history(method: Callable) -> Callable:
    """Displays the call history of a Cache class' method.
       This function retrieves the call count and i/o-put values
       for the specified meth from Redis data storage, and print
    """
    @wraps(method)
    def invoker(self, *args, **kwargs) -> Any:
        """Returns the method's output after storing product
        """
        in_key = '{}:inputs'.format(method.__qualname__)
        out_key = '{}:outputs'.format(method.__qualname__)
        redis_instance = self._redis
        while isinstance(redis_instance, redis.Redis):
            redis_instance.rpush(in_key, str(args))
            break
        output = method(self, *args, **kwargs)
        redis_instance = self._redis
        while isinstance(redis_instance, redis.Redis):
            redis_instance.rpush(out_key, output)
            break
        return output
    return invoker


def replay(fn: Callable) -> None:
    """this will definitely Displays call history of Cache method.
    """
    if fn is None or not hasattr(fn, '__self__'):
        return
    redis_store = getattr(fn.__self__, '_redis', None)
    fxn_name = fn.__qualname__
    in_key = '{}:inputs'.format(fxn_name)
    out_key = '{}:outputs'.format(fxn_name)
    fxn_call_count = 0
    while isinstance(redis_store, redis.Redis):
        if redis_store.exists(fxn_name) != 0:
            fxn_call_count = int(redis_store.get(fxn_name))
            break
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
    """Represents object for storing data.
    """
    def __init__(self) -> None:
        '''Initializes a Cache instance.
        '''
        self._redis = redis.Redis()
        self._redis.flushdb(True)

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Stores the value in Redis data storage, returns the key.
        """
        data_key = str(uuid.uuid4())
        self._redis.set(data_key, data)
        return data_key

    def get(
            self,
            key: str,
            fn: Callable = None,
            ) -> Union[str, bytes, int, float]:
        """returns a value from a Redis data storage.
        """
        data = self._redis.get(key)
        return fn(data) if fn is not None else data

    def get_str(self, key: str) -> str:
        """returns a string value from a Redis data storage.
        """
        return self.get(key, lambda x: x.decode('utf-8'))

    def get_int(self, key: str) -> int:
        """return an integer value from a Redis data storage.
        """
        return self.get(key, lambda x: int(x))
