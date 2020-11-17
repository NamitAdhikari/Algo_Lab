import unittest
from search import linear_search, binary_search

class TestLinearSearch(unittest.TestCase):

    def test_search(self):
        data = [1, 2, 3, 5, 6, 12, 7, 4, 8]
        self.assertEqual(linear_search(data, 6), 4)
        self.assertEqual(linear_search(data, 10),  -1)

    def test_searchChar(self):
        data = ['t', 'a', 'b', 'l', 'e']
        self.assertEqual(linear_search(data, 'a'), 1)


class TestBinarySearch(unittest.TestCase):

    def test_search(self):
        data = [1, 2, 3, 5, 6, 12, 7, 4, 8]
        self.assertEqual(binary_search(data, 0, len(data)-1, 6), 4)
        self.assertEqual(binary_search(data, 0, len(data)-1, 10),  -1)
    
    def test_searchChar(self):
        data = ['t', 'a', 'b', 'l', 'e', 'c', 'h', 'i', 'r']
        self.assertEqual(binary_search(data, 0, len(data)-1, 'a'), 1)


if __name__ == "__main__":
    unittest.main()

