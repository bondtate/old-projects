'''
PROJECT 5 - AVL Trees
Name: Tate Bond
PID: 55032302
'''

import random as r      # To use for testing

class Node:
    # DO NOT MODIFY THIS CLASS #
    __slots__ = 'value', 'parent', 'left', 'right', 'height'

    def __init__(self, value, parent=None, left=None, right=None):
        """
        Initialization of a node
        :param value: value stored at the node
        :param parent: the parent node
        :param left: the left child node
        :param right: the right child node
        """
        self.value = value
        self.parent = parent
        self.left = left
        self.right = right
        self.height = 0

    def __eq__(self, other):
        """
        Determine if the two nodes are equal
        :param other: the node being compared to
        :return: true if the nodes are equal, false otherwise
        """
        if type(self) is not type(other):
            return False
        return self.value == other.value

    def __str__(self):
        """String representation of a node by its value"""
        return str(self.value)

    def __repr__(self):
        """String representation of a node by its value"""
        return str(self.value)

class AVLTree:

    def __init__(self):
        # DO NOT MODIFY THIS FUNCTION #
        """
        Initializes an empty Binary Search Tree
        """
        self.root = None    # The root Node of the tree
        self.size = 0       # The number of Nodes in the tree

    def __eq__(self, other):
        # DO NOT MODIFY THIS FUNCTION #
        """
        Describe equality comparison for BSTs ('==')
        :param other: BST being compared to
        :return: True if equal, False if not equal
        """
        if self.size != other.size:
            return False
        if self.root != other.root:
            return False
        if self.root is None or other.root is None:
            return True  # Both must be None

        if self.root.left is not None and other.root.left is not None:
            r1 = self._compare(self.root.left, other.root.left)
        else:
            r1 = (self.root.left == other.root.left)
        if self.root.right is not None and other.root.right is not None:
            r2 = self._compare(self.root.right, other.root.right)
        else:
            r2 = (self.root.right == other.root.right)

        result = r1 and r2
        return result

    def _compare(self, t1, t2):
        # DO NOT MODIFY THIS FUNCTION #
        """
        Recursively compares two trees, used in __eq__.
        :param t1: root node of first tree
        :param t2: root node of second tree
        :return: True if equal, False if nott
        """
        if t1 is None or t2 is None:
            return t1 == t2
        if t1 != t2:
            return False
        result = self._compare(t1.left, t2.left) and self._compare(t1.right, t2.right)
        return result

    def visual(self):
        """
        Returns a visual representation of the AVL Tree in terms of levels
        :return: None
        """
        root = self.root
        if not root:
            print("Empty tree.")
            return
        bfs_queue = []
        track = {}
        bfs_queue.append((root, 0, root.parent))
        h = self.height(self.root)
        for i in range(h+1):
            track[i] = []
        while bfs_queue:
            node = bfs_queue.pop(0)
            track[node[1]].append(node)
            if node[0].left:
                bfs_queue.append((node[0].left, node[1] + 1, node[0]))
            if node[0].right:
                bfs_queue.append((node[0].right, node[1] + 1, node[0]))
        for i in range(h+1):
            print(f"Level {i}: ", end='')
            for node in track[i]:
                print(tuple([node[0], node[2]]), end=' ')
            print()

    ### Implement/Modify the functions below ###

    def insert(self, node, value):
        """
        -if node is not in the list add in appropriate location
         and increase tree size by 1
        :param node: The root node of the tree or subtree
        :param value: The value to be inserted into the tree
        :return: node: the input node
        """

        if node is None:
            new_node = Node(value)
            self.root = new_node
            self.size += 1
            return node

        else:
            if value > node.value:
                if node.right is None:
                    # create a new node and insert
                    new_node = Node(value)
                    new_node.parent = node
                    node.right = new_node
                    self.size += 1
                    self.rebalance(node)
                    self.update_height(node)
                    return node

                else:
                    r_node = self.insert(node.right, value)
                    self.rebalance(node)
                    self.update_height(node)
                    self.update_height(r_node)
                    return node

            elif value < node.value:
                if node.left is None:
                    # create a new node and insert
                    new_node = Node(value)
                    new_node.parent = node
                    node.left = new_node
                    self.size += 1
                    self.rebalance(node)
                    self.update_height(node)
                    return node

                else:
                    r_node = self.insert(node.left, value)
                    self.rebalance(node)
                    self.update_height(node)
                    self.update_height(r_node)
                    return node

            else:
                self.rebalance(node)
                self.update_height(node)
                return node

############################ Remove Helpler Functions ####################################

    def get_parent(self, node):
        '''
        - function to bind "remove" and "get_parent_recursive"
        - while keeping both recursive
        :param node: node to find the parent of
        :return: node: the parent of "node"
        '''
        return self.get_parent_recursive(self.root, node)

    def get_parent_recursive(self, root, node):
        '''
        - get the parent of the of the given node
        - find within the tree of the root node
        :param root: root node of tree
        :param node: node to find parent of
        :return: node: the parent of "node" param
        '''

        if root is None:
            return

        if root.left == node or root.right == node:
            return root

        elif node.value < root.value:
            return self.get_parent_recursive(root.left, node)

        else:
            return self.get_parent_recursive(root.right, node)

    def remove_node(self, parent, node):
        '''
        - remove a single node from the binary tree
        - do this based on location within tree and children
        :param parent: parent of the node to be removed
        :param node: node to be removed
        :return: True if removed False if else
        '''
        if node is None:
            return False

        # internal node 2 children
        if node.left is not None and node.right is not None:
            successor = node.left
            successor_parent = node
            while successor.right is not None:
                successor_parent = successor
                successor = successor.right

            self.remove_node(successor_parent, successor)

            node.value = successor.value

        # root with 1 or 0 children
        elif node == self.root:
            if node.left is not None:
                self.root = node.left
            else:
                self.root = node.right

        # internal with left children only
        elif node.left is not None:
            if parent.left == node:
                parent.left = node.left
            else:
                parent.right = node.left

        else:
            if parent.left == node:
                parent.left = node.right
            else:
                parent.right = node.right

        node.height = 0
        if parent is not None:
            self.rebalance(parent)
            self.update_height(parent)
            if parent.parent is not None:
                self.update_height(parent.parent)

        return True

##########################################################################################

    def remove(self, node, value):
        """
        -search the tree for the removal value
        -if found remove from tree
        -if not found do nothing
        :param node: root node of the tree or subtree
        :param value: value to search for and remove
        :return: None
        """

        if node is None:
            return
        else:
            temp_node = self.search(node, value)
            if temp_node.value == value:
                temp_node_parent = self.get_parent(temp_node)
                self.remove_node(temp_node_parent, temp_node)
                self.size -= 1
                return node
            else:
                return node

    def search(self, node, value):
        """
        - search for a given value within a tree
        - if not find give a potential parent to the node
        :param node: root node of the tree or subtree
        :param value: value to search for
        :return: the node if found the potential parent if not
        """
        if node is None:
            return
        else:

            if node.value == value:
                return node

            elif node.value < value:
                if node.right is not None:
                    return self.search(node.right, value)
                else:
                    return node

            else:
                if node.left is not None:
                    return self.search(node.left, value)
                else:
                    return node



    def inorder(self, node):
        """
        - generator object for returning nodes from an inorder traversal
        - start at param: node
        :param node: the root of the tree or subtree
        :return: a generator object containing the inorder traversal
        """

        if node is None:
            return -1

        yield from self.inorder(node.left)
        yield node
        yield from self.inorder(node.right)



    def preorder(self, node):
        """
        - generator object for returning nodes from an preorder traversal
        - start at param: node
        :param node: the root of the tree or subtree
        :return: a generator object containing the preorder traversal
        """

        if node is None:
            return -1

        yield node
        yield from self.preorder(node.left)
        yield from self.preorder(node.right)


    def postorder(self, node):
        """
        - generator object for returning nodes from an postorder traversal
        - start at param: node
        :param node: the root of the tree or subtree
        :return: a generator object containing the iorder traversal
        """

        if node is None:
            return -1

        yield from self.postorder(node.left)
        yield from self.postorder(node.right)
        yield node


    def depth(self, value):
        """
        - return the depth of the node with the given value
        :param value: value to find the depth for
        :return: -1 if empty tree or value not found depth otherwise
        """

        if self.size <= 0 or value is None:
            return -1
        else:
            node = self.root
            count = 0

            while node is not None:
                if node.value == value:
                    return count
                elif value > node.value:
                    node = node.right
                    count += 1
                elif value < node.value:
                    node = node.left
                    count += 1

            if node is None:
                return -1

    def height(self, node):
        """
        - find the height of the given node
        :param node: node to find height of
        :return: int: the height of the tree
        """
        if node is None or self.size <= 0:
            return -1
        else:
            return node.height


    def min(self, node):
        """
        - work down to the farthest left node recursively
        :param node: root of tree or subtree
        :return: node: the minimum node value
        """
        if node is None:
            return

        else:

            if node.left is None:
                return node

            else:
                return self.min(node.left)


    def max(self, node):
        """
        - work down to the farthest right node recursively
        :param node: root of tree or subtree
        :return: node: the maximum node value
        """
        if node is None:
            return

        else:

            if node.right is None:
                return node

            else:
                return self.max(node.right)


    def get_size(self):
        """
        - return the number of nodes in the tree "self.size"
        :return: int the number of nodes in the tree
        """
        return self.size


    def get_balance(self, node):
        """
        - return the balance factor of the given tree
        - balance factor = left.height - right.height
        :param node: root of the tree or subtree
        :return: int: the baclance factor of the tree
        """

        if node is None:
            return 0
        else:
            left_height = -1
            right_height = -1
            if node.left is not None:
                left_height = node.left.height
            elif node.right is not None:
                right_height = node.right.height
            return left_height - right_height

    ########################### ROTATE HELPER FUNCTIONS ###########################

    def update_height(self, node):
        '''
        - Update the current height of the node
        :param node: node to update height
        :return: None
        '''
        left = -1
        if node.left is not None:
            left = node.left.height
        right = -1
        if node.right is not None:
            right = node.right.height
        node.height = max(left, right) + 1

    def set_child(self, parent, which_child, child):
        '''
        - set parents "which_child" to the given child
        :param parent: parent to assign new child
        :param which_child: directional child either left or right
        :param child: the new child of parent
        :return: True if successful False if else
        '''
        if which_child != "left" and which_child != "right":
            return False
        if which_child == "left":
            parent.left = child
        else:
            parent.right = child
        if child is not None:
            child.parent = parent
        self.update_height(parent)
        return True

    def replace_child(self, parent, current_child, new_child):
        '''
        - replace a current child with a given child
        :param parent: new parent of new_child
        :param current_child: current node with "parent" as parent node
        :param new_child: new child to have "parent" as parent node
        :return: True if successful False if else
        '''
        if parent.left == current_child:
            return self.set_child(parent, "left", new_child)
        elif parent.right == current_child:
            return self.set_child(parent, "right", new_child)

        return False

    def get_balance(self, node):
        '''
        - find the current balance of the given node
        - balance = left.height - right.height
        :param node: input node of to find balance of
        :return: the current balance of the node
        '''
        left = -1
        right = -1
        if node.left is not None:
            left = node.left.height
        if node.right is not None:
            right = node.right.height

        return left - right

    ###############################################################################

    def left_rotate(self, root):
        """
        - perform a left rotation using the given root
        :param root: the root node of the tree or subtree
        :return: None
        """

        if root is None or root.right is None:
            return
        else:
            right_left_child = root.right.left
            if root.parent is not None:
                self.replace_child(root.parent, root, root.right)
            else:
                self.root = root.right
                self.root.parent = None

            self.set_child(root.right, "left", root)
            self.set_child(root, "right", right_left_child)



    def right_rotate(self, root):
        """
        - perform a right rotation using the given root
        - mirror of left_rotate()
        :param root: the root node of the tree or subtree
        :return: None
        """

        if root is None or root.left is None:
            return
        else:
            left_right_child = root.left.right
            if root.parent is not None:
                self.replace_child(root.parent, root, root.left)
            else:
                self.root = root.left
                self.root.parent = None

            self.set_child(root.left, "right", root)
            self.set_child(root, "left", left_right_child)


    def rebalance(self, node):
        """
        - rebalance the given tree based at the root node
        - perform rotations based on the current balance
        :param node: root of the tree or sub-tree
        :return: the new root node of the tree
        """

        if node is None:
            return
        else:
            self.update_height(node)
            if self.get_balance(node) == -2:
                if self.get_balance(node.right) == 1:
                    self.right_rotate(node.right)
                return self.left_rotate(node)

            elif self.get_balance(node) == 2:
                if self.get_balance(node.left) == -1:
                    self.left_rotate(node.left)
                return self.right_rotate(node)


            return node

def swap_nodes(node1, node2):
    '''
    - swap the values of two nodes
    :param node1: node to be swapped
    :param node2: node to be swapped
    :return: Void
    '''

    if node1 is None or node2 is None:
        return

    else:
        temp_val = node1.value
        node1.value = node2.value
        node2.value = temp_val

def repair_tree(tree):
    """
    - checks if tree is broken (2 values in wrong location)
    - swaps them into the right location using "swap_nodes"
    :param tree: tree to be repaired
    :return: Void
    """

    if tree.root is None:
        return
    else:

        generator = tree.inorder(tree.root)
        prev_node = tree.min(tree.root)
        swap1 = None
        swap2 = None

        for node in generator:
            if node.value < prev_node.value:
                swap1 = prev_node
                swap2 = node
                prev_node = node
                break

            prev_node = node

        for node in generator:
            if node.value < prev_node.value:
                swap2 = node
                break

            prev_node = node

    swap_nodes(swap1, swap2)



def main():



    tree = AVLTree()

    tree.insert(tree.root, 10)
    tree.insert(tree.root, 5)
    tree.insert(tree.root, 12)
    tree.insert(tree.root, 6)
    tree.insert(tree.root, 11)
    tree.insert(tree.root, 4)
    tree.insert(tree.root, 16)
    print(tree.depth(12))
    tree.visual()
    print()

    ####################################

    avl = AVLTree()

    node_root = Node(10)
    node_root.height = 3

    node_l = Node(6)
    node_l.height = 2
    node_l.parent = node_root
    node_root.left = node_l

    node_ll = Node(5)
    node_ll.height = 1
    node_ll.parent = node_l
    node_l.left = node_ll

    node_lll = Node(4)
    node_lll.height = 0
    node_lll.parent = node_ll
    node_ll.left = node_lll

    node_r = Node(11)
    node_r.height = 2
    node_r.parent = node_root
    node_root.right = node_r

    node_rr = Node(15)
    node_r.height = 1
    node_rr.parent = node_r
    node_r.right = node_rr

    node_rrr = Node(12)
    node_r.height = 0
    node_rrr.parent = node_rr
    node_rr.right = node_rrr
    ###################################

    avl.root = node_root
    avl.size = 7

    repair_tree(avl)
    avl.visual()



    '''avl = AVLTree()

    avl.insert(avl.root, 21)
    avl.insert(avl.root, 10)
    avl.insert(avl.root, 32)
    avl.insert(avl.root, 5)
    avl.insert(avl.root, 16)
    avl.insert(avl.root, 27)
    avl.insert(avl.root, 39)
    avl.insert(avl.root, 1)

    avl.visual()

    avl2 = AVLTree()
    avl2.insert(avl2.root, 10)

    print(avl2.height(avl2.root))
    print(avl2.depth(5))

    assert avl.depth(1) == 3
    assert avl.depth(10) == 1

    assert avl.height(avl.root) == 3
    assert avl.height(avl.root.left) == 2'''


if __name__ == '__main__':
    main()