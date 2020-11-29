import unittest
from bst import BinarySearchTree

class BSTTestCase(unittest.TestCase):

    def setUp(self):
        """
        Executed before each test method.
        Before each test method, create a BST with some fixed key-values.
        """
        self.bst = BinarySearchTree()
        self.bst.add(10, "Value for 10")
        self.bst.add(52, "Value for 52")
        self.bst.add(5, "Value for 5")
        self.bst.add(8, "Value for 8")
        self.bst.add(1, "Value for 1")
        self.bst.add(40, "Value for 40")
        self.bst.add(30, "Value for 30")
        self.bst.add(45, "Value for 45")

    def test_add(self):
        """
        tests for add
        """
        # Create an instance of BinarySearchTree
        bsTree = BinarySearchTree()

        # bsTree must be empty
        self.assertEqual(bsTree.size(), 0)

        # Add a key-value pair
        bsTree.add(15, "Value for 15")
        # Size of bsTree must be 1
        self.assertEqual(bsTree.size(), 1)

        # Add another key-value pair
        bsTree.add(10, "Value for 10")
        # Size of bsTree must be 2
        self.assertEqual(bsTree.size(), 2)

        # The added keys must exist.
        self.assertEqual(bsTree.search(10), "Value for 10")
        self.assertEqual(bsTree.search(15), "Value for 15")

    def test_inorder(self):
        """
        tests for inorder_walk
        """
        self.assertListEqual(self.bst.inorder_walk(), [1, 5, 8, 10, 30, 40, 45, 52])

        # Add one node
        self.bst.add(25, "Value for 25")
        # Inorder traversal must return a different sequence
        self.assertListEqual(self.bst.inorder_walk(), [1, 5, 8, 10, 25, 30, 40, 45, 52])

    def test_postorder(self):
        """
        tests for postorder_walk
        """
        self.assertListEqual(self.bst.postorder_walk(), [1, 8, 5, 30, 45, 40, 52, 10])

        # Add one node
        self.bst.add(25, "Value for 25")
        # Inorder traversal must return a different sequence
        self.assertListEqual(self.bst.postorder_walk(), [1, 8, 5, 25, 30, 45, 40, 52, 10])

    def test_preorder(self):
        """
        tests for preorder_walk
        """
        self.assertListEqual(self.bst.preorder_walk(), [10, 5, 1, 8, 52, 40, 30, 45])

        # Add one node
        self.bst.add(25, "Value for 25")
        # Inorder traversal must return a different sequence
        self.assertListEqual(self.bst.preorder_walk(), [10, 5, 1, 8, 52, 40, 30, 25, 45])

    def test_search(self):
        """
        tests for search
        """
        self.assertEqual(self.bst.search(40), "Value for 40")

        self.assertFalse(self.bst.search(90))

        self.bst.add(90, "Value for 90")
        self.assertEqual(self.bst.search(90), "Value for 90")

    def test_remove(self):
        """
        tests for remove
        """
        self.bst.remove(40)

        self.assertEqual(self.bst.size(), 7)
        self.assertListEqual(self.bst.inorder_walk(), [1, 5, 8, 10, 30, 45, 52])
        self.assertListEqual(self.bst.postorder_walk(), [1, 8, 5, 30, 45, 52, 10])
        self.assertListEqual(self.bst.preorder_walk(), [10, 5, 1, 8, 52, 45, 30])


    def test_smallest(self):
        """
        tests for smallest
        """
        self.assertTupleEqual(self.bst.smallest(), (1, "Value for 1"))

        # Add some nodes
        self.bst.add(6, "Value for 6")
        self.bst.add(4, "Value for 4")
        self.bst.add(0, "Value for 0")
        self.bst.add(32, "Value for 32")

        # Now the smallest key is 0.
        self.assertTupleEqual(self.bst.smallest(), (0, "Value for 0"))

    def test_largest(self):
        """
        tests for largest
        """
        self.assertTupleEqual(self.bst.largest(), (52, "Value for 52"))

        # Add some nodes
        self.bst.add(6, "Value for 6")
        self.bst.add(54, "Value for 54")
        self.bst.add(0, "Value for 0")
        self.bst.add(32, "Value for 32")

        # Now the largest key is 54
        self.assertTupleEqual(self.bst.largest(), (54, "Value for 54"))

if __name__ == "__main__":
    unittest.main()
