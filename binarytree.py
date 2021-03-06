#!/usr/bin/env python3
from collections import deque


class BinaryTree(object):
    '''
    A binary tree.
    '''

    def __init__(self):
        self.root = None

    def __repr__(self):
        return repr(self.root)

    def set(self, key, value):
        '''
        Adds the given key=value pair to the tree.
        '''
        if self.root:
            # set root further down
            self._set(key, value, self.root)
        else:
            # set root node is it hasn't been set already
            self.root = Node(None, key, value)

    def get(self, key):
        '''
        Retrieves the value under the given key.
        Returns None if the key does not exist.
        '''
        if self.root:
            value = self._get(key, self.root)
            if value:
                return value
            else:
                return None
        else:
            return None

    def remove(self, key):
        '''
        Removes the given key from the tree.
        Returns silently if the key does not exist.
        '''
        if self.root == None:
            return

        def recurse(current, key):
            # found node to delete
            if current.key == key:
                if current.left is not None and current.right is not None:
                    # print("2 leaves")
                    # print(f"for key {current.key}")
                    [min_parent_node, min_node] = current.right._find_min(
                        current.parent)
                    # get rid of the min node
                    if min_parent_node.left == min_node:
                        min_parent_node.left = min_node.right
                    else:
                        min_parent_node.right = min_node.right

                    # set min_node at replace level
                    min_node.left = current.left
                    min_node.right = current.right
                    current.value = min_node.value
                    current.key = min_node.key

                    # return the min_node's tree to get out of recursion
                    return min_node
                elif current.left is not None or current.right is not None:
                    # print("1 leaf")
                    # print(f"for key {current.key}")
                    # return/promote tree from correct side
                    if current.left:
                        if current.parent.left and current.parent.left.key == current.key:
                            current.parent.left = current.left
                        elif current.parent.right and current.parent.right.key == current.key:
                            current.parent.right = current.right
                        return current.left
                    else:
                        if current.parent.left and current.parent.left.key == current.key:
                            current.parent.left = current.left
                        elif current.parent.right and current.parent.right.key == current.key:
                            current.parent.right = current.right
                        return current.right
                else:
                    # print("0 leaves")
                    # print(f"for key {current.key}")
                    if current.parent.left and current.parent.left.key == current.key:
                        current.parent.left = None
                    elif current.parent.right and current.parent.right.key == current.key:
                        current.parent.right = None
                    return current
            else:
                # key is to the left of this section of the tree
                if current.key > key:
                    if current.left:
                        recurse(current.left, key)
                # key is to the right of this section of the tree
                else:
                    if current.right:
                        recurse(current.right, key)

        recurse(self.root, key)
        return None

    def walk_dfs_inorder(self):
        '''
        An iterator that walks the tree in DFS fashion.
        Yields (key, value) for each node in the tree.
        '''
        if self.root == None:
            return

        def recurse(current):
            if not current:
                return
            if current._has_left_child:
                yield from recurse(current.left)
            yield (current.key, current.value)
            if current._has_right_child:
                yield from recurse(current.right)

        yield from recurse(self.root)

    def walk_dfs_preorder(self, node=None, level=0):
        '''
        An iterator that walks the tree in preorder DFS fashion.
        Yields (key, value) for each node in the tree.
        '''
        if self.root == None:
            return

        def recurse(current):
            if not current:
                return
            yield (current.key, current.value)
            if current._has_left_child:
                yield from recurse(current.left)
            if current._has_right_child:
                yield from recurse(current.right)

        yield from recurse(self.root)

    def walk_dfs_postorder(self, node=None, level=0):
        '''
        An iterator that walks the tree in inorder DFS fashion.
        Yields (key, value) for each node in the tree.
        '''
        if self.root == None:
            return

        def recurse(current):
            if not current:
                return
            if current._has_left_child:
                yield from recurse(current.left)
            if current._has_right_child:
                yield from recurse(current.right)
            yield (current.key, current.value)

        yield from recurse(self.root)

    def walk_bfs(self):
        '''
        An iterator that walks the tree in BFS fashion.
        Yields (key, value) for each node in the tree.
        '''
        to_visit = []
        if self.root == None:
            return
        to_visit.append(self.root)
        while to_visit:
            current = to_visit.pop(0)
            yield (current.key, current.value)
            if current.left:
                to_visit.append(current.left)
            if current.right:
                to_visit.append(current.right)

    ##################################################
    # Helper methods

    def _replace_node(self, oldnode, newnode):
        '''
        Internal method to remove a node from its parent
        '''
        # TODO: feel free to use or remove this method

    def _find(self, key):
        '''
        Internal method to find a node by key.
        Returns (parent, node).
        '''
        # TODO: feel free to use or remove this method

    def _set(self, key, value, current):
        '''
        Adds the given key=value pair to the tree.
        '''
        if key < current.key:
            if current._has_left_child():
                self._set(key, value, current.left)
            else:
                current.left = Node(current, key, value)
        else:
            if current._has_right_child():
                self._set(key, value, current.right)
            else:
                current.right = Node(current, key, value)

    def _get(self, key, current):
        if not current:
            return None
        elif current.key == key:
            return current.value
        elif key < current.key:
            return self._get(key, current.left)
        else:
            return self._get(key, current.right)


class Node(object):
    '''
    A node in a binary tree.
    '''

    def __init__(self, parent, key, value):
        '''Creates a linked list.'''
        self.key = key
        self.value = value
        self.parent = parent
        self.left = None
        self.right = None

    def __repr__(self):
        result = []

        def recurse(node, prefix1, side, prefix2):
            if node is None:
                return
            result.append(prefix1 + node.key + side)
            if node.right is not None:
                recurse(node.left, prefix2 + '\u251c\u2500\u2500 ',
                        ' \u2c96', prefix2 + '\u2502   ')
            else:
                recurse(node.left, prefix2 + '\u2514\u2500\u2500 ',
                        ' \u2c96', prefix2 + '    ')
            recurse(node.right, prefix2 + '\u2514\u2500\u2500 ',
                    ' \u1fe5', prefix2 + '    ')
        recurse(self, '', '', '')
        return '\n'.join(result)

    def _has_left_child(self):
        return self.left

    def _has_right_child(self):
        return self.right

    def _find_min(self, parent):
        """ return the minimum node in the current tree and its parent """
        if self.left:
            return self.left._find_min(self)
        else:
            return [parent, self]
