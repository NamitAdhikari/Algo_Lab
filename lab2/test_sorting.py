import unittest
from insert import insertionSort
from merge import mergeSort

class SortingTestCase(unittest.TestCase):
    def test_insertion_sort(self):
        input = [3, 1, 9, 4, 2, 7, 6, 10, 8, 5]
        output = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

        insertionSort(input)

        self.assertListEqual(input, output)

    def test_merge_sort(self):
        input = [3, 1, 9, 4, 2, 7, 6, 10, 8, 5]
        output = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

        mergeSort(input, 0, len(input)-1)

        self.assertListEqual(input, output)

if __name__ == "__main__":
    unittest.main()
