#!/usr/bin/env python3
"""
Deletion-resilient hypermedia pagination
"""
from base_caching import BaseCaching
from collections import OrderedDict


class MRUCache(BaseCaching):
    """ MRUCache class """

    def __init__(self):
        """ init method """
        super().__init__()
        self.cache_data = OrderedDict()

    def put(self, key, item):
        """ add key/item pair to the cache dict """
        if key and item:
            if key not in self.cache_data:
                if len(self.cache_data) + 1 > self.MAX_ITEMS:
                    removed_key, _ = self.cache_data.popitem(True)
                    print(f"DISCARD: {removed_key}")
            self.cache_data[key] = item
            self.cache_data.move_to_end(key, last=True)

    def get(self, key):
        """ Get an item from cache dict by key """
        if key and key in self.cache_data:
            self.cache_data.move_to_end(key, last=True)
            return self.cache_data.get(key)

