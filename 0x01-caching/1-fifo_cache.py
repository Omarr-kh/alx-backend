#!/usr/bin/env python3
"""
Deletion-resilient hypermedia pagination
"""
from base_caching import BaseCaching
from collections import OrderedDict


class FIFOCache(BaseCaching):
    """ FIFOCache class """

    def __init__(self):
        """ init method """
        super().__init__()
        self.cache_data = OrderedDict()

    def put(self, key, item):
        """ add key/item pair to the cache dict """
        if key and item:
            self.cache_data[key] = item
            if len(self.cache_data) > self.MAX_ITEMS:
                removed_key, val = self.cache_data.popitem(False)
                print(f"DISCARD: {removed_key}")

    def get(self, key):
        """ Get an item from cache dict by key """
        return self.cache_data.get(key)
