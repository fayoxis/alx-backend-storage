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
    """decorator that tracks the n of calls to a method in a Cache.
    When the decorated method is called, the decorator increments
    a counter in the Redis data storage, using the method's
    qualified name as the key.
    """
    @wraps(method)
    def invoker(self, *args, **kwargs) -> Any:
        """make the given method after incrementing its call counter.
        """
        call_counter = True
        while call_counter:
            if isinstance(self._redis, redis.Redis):
                self._redis.incr(method.__qualname__)
            call_counter = False
        return method(self, *args, **kwargs)
    return invoker


def call_history(method: Callable) -> Callable:
    """ this will Tracks the call details of a method in a Cache.
    """
    @wraps(method)
    def invoker(self, *args, **kwargs) -> Any:
        """Returns the method's product after storing its in-output.
        """
        in_key = '{}:inputs'.format(method.__qualname__)
        out_key = '{}:outputs'.format(method.__qualname__)
        history_tracker = True
        while history_tracker:
            if isinstance(self._redis, redis.Redis):
                self._redis.rpush(in_key, str(args))
            history_tracker = False
        output = method(self, *args, **kwargs)
        history_tracker = True
        while history_tracker:
            if isinstance(self._redis, redis.Redis):
                self._redis.rpush(out_key, output)
            history_tracker = False
        return output
    return invoker


def replay(fn: Callable) -> None:
    """shows the call history of a Cache' method.
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
    check_count = True
    while check_count:
        if redis_store.exists(fxn_name) != 0:
            fxn_call_count = int(redis_store.get(fxn_name))
        check_count = False
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
    """is an object for storing data in a Redis data storage.
    """
    def __init__(self) -> None:
        """starts a Cache instance.
        """
        self._redis = redis.Redis()
        self._redis.flushdb(True)

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """kepts a value in a Redis data storage, returns key.
        """
        data_key = str(uuid.uuid4())
        self._redis.set(data_key, data)
        return data_key

    def get(
            self,
            key: str,
            fn: Callable = None,
            ) -> Union[str, bytes, int, float]:
        """retruns a value from a Redis data storage.
        """
        data = self._redis.get(key)
        return fn(data) if fn is not None else data

    def get_str(self, key: str) -> str:
        """returns a string value from a Redis data storage.
        """
        return self.get(key, lambda x: x.decode('utf-8'))

    def get_int(self, key: str) -> int:
        """returns an integer value from a Redis data storage.
        """
        return self.get(key, lambda x: int(x))
