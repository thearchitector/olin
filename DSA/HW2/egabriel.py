"""
Implements a doubly-linked list with deletion, insertion, pushing, and multiplicative functionality.

@author: Elias Gabriel
@revision: v1.1.0
"""
import itertools

class Node:
    def __init__(self,val=None,nxt=None,prev=None):
        self.val = val
        self.next = nxt
        self.prev = prev

class DLL:
    def __init__(self):
        """ Initalizes an empty doubly-linked list. """
        self.size = 0
        self.firstNode = None
        self.lastNode = None
        self.sum = 0

    def length(self):
        """ Returns the number of nodes in the list. """
        return self.size

    def __update_internal__(self, delsize, delsum):
        self.size += delsize
        self.sum += delsum

    def push(self, val):
        """ Adds a node with value equal to val to the front of the list. """
        # Create a new node
        node = Node(val=val, nxt=self.firstNode)

        # If there is a node in the list
        if self.firstNode:
            # Set the old first node's new first to the new node 
            self.firstNode.prev = node
        else:
            # If there is no first, the new node is both the first and last
            self.lastNode = node

        # Update the first node and list size
        self.firstNode = node
        self.__update_internal__(1, val)

    def insert_after(self, prev_node, val):
        """ Adds a node with value equal to val in the list after prev_node. """
        # Create the new node and insert it into the list
        n = Node(val=val, nxt=prev_node.next, prev=prev_node)
        # Update the rest of the chain's pointers correspondingly
        if prev_node.next: prev_node.next.prev = n
        prev_node.next = n

        # Update the last node if necessary
        if prev_node == self.lastNode:
            self.lastNode = n

        # Update the internal size and sum
        self.__update_internal__(1, val)

    def delete(self, node):
        """ Removes the specified node from the list. """
        # Update the node's links so that it is no longer part of the chain
        if node is not self.lastNode: node.next.prev = node.prev
        if node is not self.firstNode: node.prev.next = node.next

        # Update the first and last nodes if necessary
        if node == self.firstNode:
            self.firstNode = node.next
        
        if node == self.lastNode:
            self.lastNode = node.prev

        # Update the internal size and sum
        self.__update_internal__(-1, -node.val)

    def index(self, i):
        """
        Returns the node at position i (i<n). Searchs from the most optimal direction
        for the given index.
        """
        if i >= self.size:
            raise IndexError("list index out of range")
        elif i < self.size / 2:
            # If the index is in the front half of the list, just count up to it
            n = self.firstNode
            for j in range(i): n = n.next
        else:
            # If the index if the the second half of the list, count backwards to
            # reduce unnecessary steps
            n = self.lastNode
            for j in range(self.size - i - 1): n = n.prev
        
        return n

    def multiply_all_pairs(self):
        """ Multiplies all unique pairs of nodes and returns the sum. """
        prodsum = 0
        s = self.sum
        n = self.firstNode

        # Loop through all the nodes in the list, calculating the rolling product sum
        # along the way. Takes advantage of the distributive principle. For [a,b,c,d]
        # the pair products are [ab, ac, ad, bc, bd, cd], which can be rearranged as:
        #   a(b + c + d) + b(c + d) + cd
        # Making use of this yields a runtime of O(N).
        while n:
            s -= n.val
            prodsum += n.val * s
            n = n.next

        return prodsum


###
### TEST SECTION
###


def test_dll_initialization():
    """ Checks whether instantiation was successful. """
    assert DLL() is not None

def test_dll_index():
    """ Checks whether list indexing works. """
    dll = DLL()
    dll.push(42)
    dll.push(41)
    dll.push(40)
    assert dll.index(0).val == 40
    assert dll.index(1).val == 41
    assert dll.index(2).val == 42

def test_dll_push():
    """ Checks whether the push operation was successful. """
    dll = DLL()
    dll.push(42)
    assert dll.length() == 1
    assert dll.index(0).val == 42

def test_dll_insert():
    """ Checks whether the insertion was successful. """
    dll = DLL()
    dll.push(42)
    dll.push(40)
    dll.insert_after(dll.firstNode, 41)
    n = dll.index(1)
    assert dll.firstNode.val == 40
    assert dll.lastNode.val == 42
    assert n.val == 41
    assert n.prev == dll.firstNode
    assert n.next == dll.lastNode

def test_dll_delete():
    """ Tests whether or not deletion works. """
    dll = DLL()
    dll.push(42)
    dll.push(41)
    dll.push(40)
    dll.delete(dll.index(0))
    assert dll.firstNode.val == 41
    assert dll.length() == 2

def test_dll_multiply():
    """ Tests whether or not pair-wise rolling product summation works. """
    dll = DLL()
    dll.push(3)
    dll.push(2)
    dll.push(1)
    assert dll.multiply_all_pairs() == 11
    dll.push(9)
    dll.insert_after(dll.index(2), 7)
    assert dll.multiply_all_pairs() == 170


###
### PERFORMANCE SECTION
###


import seaborn as sns
import matplotlib.pyplot as plt
import random
import timeit

if __name__ == "__main__":
    sns.set(style="darkgrid")
    f = plt.figure()
    xs = range(10, 10001, 10)
    ys1 = []
    ys2 = []
    ys3 = []

    # Time DLL indexing and pairwise multiplication
    for n in xs:
        l = DLL()
        m = list(range(n))

        for i in range(n): l.push(i)

        ys1.append((timeit.timeit("l.index(random.randrange(n))", "import random", number=50, globals=locals()) / 50) * 1000)
        ys2.append((timeit.timeit("l.multiply_all_pairs()", number=50, globals=locals()) / 50) * 1000)
        ys3.append((timeit.timeit("m[random.randrange(n)]", "import random", number=50, globals=locals()) / 50) * 1000)


    # Plot the results
    plt.plot(xs, ys1)
    plt.title("Indexing Performance vs. DLL Size")
    plt.xlabel("list size")
    plt.ylabel("time (ms)")
    plt.show()

    plt.plot(xs, ys3)
    plt.title("Indexing Performance vs. List Size")
    plt.xlabel("list size")
    plt.ylabel("time (ms)")
    plt.show()

    plt.plot(xs, ys2)
    plt.title("Pair Multiplication vs List Size")
    plt.xlabel("list size")
    plt.ylabel("time (ms)")
    plt.show()


