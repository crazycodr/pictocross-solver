import redis
import json
import os
import logging

class Cache:

    def save(self, key, data):
        pass

    def retrieve(self, key):
        pass

    def hasKey(self, key) -> bool:
        pass

class MemoryCache(Cache):

    def __init__(self):
        self._data = {}

    def save(self, key, data):
        self._data[key] = data

    def retrieve(self, key):
        return self._data[key]

    def hasKey(self, key) -> bool:
        return key in self._data

class RedisCache(Cache):

    def __init__(self, host: str, port: int):
        self._redis = redis.StrictRedis(host=host, port=port, db=0, decode_responses=True)

    def save(self, key, data):
        self._redis.lpush(key, *data)

    def retrieve(self, key):
        return self._redis.lrange(key, 0, -1)

    def hasKey(self, key) -> bool:
        return self._redis.exists(key)

class FileCache(Cache):

    def __init__(self, directory: str):
        self._directory = directory

    def save(self, key, data):
        logging.debug(f'Saving {key} to filesystem file: {self._directory + "/cache-file_" + str(key) + ".json"}')
        with open(self._directory + '/cache-file_' + str(key) + '.json', 'w') as json_file:  
            json.dump(data, json_file)

    def retrieve(self, key):
        logging.debug(f'Loading {key} from filesystem file: {self._directory + "/cache-file_" + str(key) + ".json"}')
        with open(self._directory + '/cache-file_' + str(key) + '.json', 'r') as json_file:
            return json.loads(json_file.read())

    def hasKey(self, key) -> bool:
        return os.path.exists(self._directory + '/cache-file_' + str(key) + '.json')
    
class CacheChain(Cache):
    """
    Cache chain receives multiple cache handlers and tries to call the cache method
    on each underlying helper until it succeeds
    """

    def __init__(self):
        self._caches = []
    
    def addCache(self, cache: Cache):
        """
        Adds a cache helper to the chain
        """
        self._caches.append(cache)

    def save(self, key, data):
        """
        When saving, the cache chain should save to all cache handlers.
        """
        for cache in self._caches:
            cache.save(key, data)

    def retrieve(self, key):
        """
        When loading, the cache should attempt to retrieve the key from
        the first available cache and move on until something is found.
        """
        skippedCaches = []
        for cache in self._caches:
            if cache.hasKey(key):
                data = cache.retrieve(key)
                for skippedCache in skippedCaches:
                    skippedCache.save(key, data)
                return data
            else:
                skippedCaches.append(cache)

    def hasKey(self, key) -> bool:
        for cache in self._caches:
            if cache.hasKey(key):
                return True
        return False