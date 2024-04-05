#!/usr/bin/env python3
""" index_range function """
import csv
import math
from typing import Tuple, List, Dict


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

    def get_hyper(self, page: int = 1, page_size: int = 10) -> Dict:
        """ returns a dictionary
        containing the following key-value pairs:

            page_size: the length of the returned dataset page
            page: the current page number
            data: the dataset page (equivalent to return from previous task)
            next_page: number of the next page, None if no next page
            prev_page: number of the previous page, None if no previous page
            total_pages: the total number of pages in the dataset as an int
        """

        data = self.get_page(page, page_size)

        total_pages = math.ceil(len(self.__dataset) / page_size)
        next_page = page + 1 if page + 1 < total_pages else None
        prev_page = page - 1 if page - 1 > 0 else None

        return {
            "page_size": page_size,
            "page": page,
            "data": data,
            "next_page": next_page,
            "prev_page": prev_page,
            "total_pages": total_pages
        }
