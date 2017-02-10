class TreeNode:
    def __init__(self, value):
        self.left = None
        self.right = None

        self.value = value

class InnerTree:
    def __init__(self, value, binaryTree):
        self.value = value
        self.binaryTree = binaryTree

class BinarySearchTree:
    def __init__(self):
        self.root = None
        self.size = 0

    def insert(self, value):
        node = self.root
        newNode = TreeNode(value)

        if node:
            prevNode = None

            while node:
                prevNode = node;
                if cmpValues(newNode.value, node.value):
                    node = node.left
                else:
                    node = node.right

            if cmpValues(newNode.value, prevNode.value):
                prevNode.left = newNode
            else:
                prevNode.right = newNode
        else:
            self.root = newNode

def cmpValues(lhs, rhs):
    if type(lhs) == InnerTree:
        return lhs.value < rhs.value
    else :
        return lhs < rhs
