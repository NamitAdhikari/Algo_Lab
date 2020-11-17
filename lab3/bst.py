class BinarySearchTree:

    def __init__(self, key=0, value=0):
        self.root = None
        self._size = 0

    class BSTNode:
        def __init__(self, key, value):
            self.key = key
            self.value = value
            self.right = None
            self.left = None


    # Add a node to the BST
    def add(self, key, value):
        z = self.BSTNode(key, value)
        y = None
        x = self.root

        while (x != None):
            y = x
            if (z.key < x.key):
                x = x.left
            else:
                x = x.right

        if (y == None):
            self.root = z
        elif (z.key < y.key):
            y.left = z
        else:
            y.right = z

        self._size += 1

    # Return the number of nodes in the BST
    def size(self):
        return self._size

    # Perform inorder traversal. Must return a list of keys visited in inorder way, e.g. [1, 2, 3, 4].
    def inorder_walk(self):
        stack = []
        list = []
        x = self.root

        while stack or x:
            if x:
                stack.append(x)
                x = x.left
            else:
                x = stack.pop()
                list.append(x.key)
                x = x.right

        return list


    # Perform postorder traversal. Must return a list of keys visited in inorder way, e.g. [1, 4, 3, 2].
    def postorder_walk(self):
        x = self.root
        stack = []
        stack.append(x)
        list = []

        while stack:
            x = stack.pop()
            list.append(x.key)

            if x.left:
                stack.append(x.left)

            if x.right:
                stack.append(x.right)

        list = list[::-1]

        return list

    # Perform preorder traversal. Must return a list of keys visited in inorder way, e.g. [2, 1, 3, 4].
    def preorder_walk(self):
        x = self.root

        stack = []
        stack.append(x)

        list = []
        while stack:
            x = stack.pop()
            list.append(x.key)
            if x.right:
                stack.append(x.right)
            if x.left:
                stack.append(x.left)

        return list

    # Search the BST for the given key. Return False if the key is not found.
    def search(self, key):
        x = self.root
        while x != None:
            if key == x.key:
                return x.value
            elif key < x.key:
                x = x.left
            else:
                x = x.right
        return False

    # Remove a key from the BST. Return False if the key is not present in the BST.
    def remove(self, key):
        x = self.root
        y = None

        while (x != None and x.key != key):
            y = x
            if key < x.key:
                x = x.left
            else:
                x = x.right

        if x == None:
            return

        if x.left == None or x.right == None:
            z = None

            if x.left == None:
                z = x.right
            else:
                z = x.left

            if y == None:
                return

            if x == y.left:
                y.left = z
            else:
                y.right = z

            x = None

        else:
            p = None
            temp = None

            temp = x.right
            while (temp.left != None):
                p = temp
                temp = temp.left

            if p != None:
                p.left = temp.right
            else:
                x.right = temp.right

            x.key = temp.key
            temp = None
            self._size -= 1



    # Find the smallest key and return the corresponding key-value pair/tuple, i.e. (key, value)
    def smallest(self):
        x = self.root
        while x.left != None:
            x = x.left

        return (x.key, x.value)


    # Find the largest key and return the corresponding key-value pair/tuple, i.e. (key, value)
    def largest(self):
        x = self.root
        while x.right != None:
            x = x.right

        return (x.key, x.value)
