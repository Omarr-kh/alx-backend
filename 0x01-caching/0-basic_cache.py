#!/usr/bin/env python3
"""
Deletion-resilient hypermedia pagination
"""
from base_caching import BaseCaching


class BasicCache(BaseCaching):
    """ BasicCache class (unlimited) """

    def put(self, key, item):
        """ add key/item pair to the cache dict """
        if key and item:
            self.cache_data[key] = item

    def get(self, key):
        """ Get an item from cache dict by key """
        return self.cache_data.get(key)
