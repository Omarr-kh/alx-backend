#!/usr/bin/env python3
""" index_range function """
import csv
import math
from typing import Tuple, List


def index_range(page: int, page_size: int) -> Tuple:
    """ Returns  a tuple of size two containing a start index and
    an end index corresponding to the range of indexes to return
    in a list for those particular pagination parameters.
    """

    start_index = (page - 1) * page_size
    end_index = start_index + page_size

    return (start_index, end_index)


class Server:
    """Server class to paginate a database of popular baby names.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None

    def dataset(self) -> List[List]:
        """Cached dataset
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def get_page(self, page: int = 1, page_size: int = 10) -> List[List]:
        """ find the correct indexes to
        paginate the dataset correctly and return the
        appropriate page of the dataset """

        assert type(page) == int and page > 0
        assert type(page_size) == int and page_size > 0

        data = self.dataset()

        start_idx, end_idx = index_range(page, page_size)

        if start_idx > len(data) - 1:
            return []

        if end_idx > len(data) - 1:
            return data[start_idx:]
        else:
            return data[start_idx: end_idx]
