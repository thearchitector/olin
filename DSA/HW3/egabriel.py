"""
Implements a queue with minimum-value tracking capabailities using a doubly-linked list.

@author: Elias Gabriel
@revision: v1.0.0
"""
import itertools

class DLL:
    class Node:
        """
        Defines a structure for holding pointer references and values.
        """
        def __init__(self,val=None,nxt=None,prev=None):
            self.val = val
            self.next = nxt
            self.prev = prev

    def __init__(self):
        """ Initalizes an empty doubly-linked list. """
        self.size = 0
        self.head = None
        self.tail = None

    def __len__(self):
        """ Returns the number of nodes in the list. """
        return self.size

    def push(self, val):
        """ Adds a node with value equal to val to the front of the list. """
        # Create a new node
        node = DLL.Node(val=val, nxt=self.head)

        # If there is a node in the list
        if self.head:
            # Set the old first node's new first to the new node 
            self.head.prev = node
        else:
            # If there is no first, the new node is both the first and last
            self.tail = node

        # Update the first node and list size
        self.head = node
        self.size += 1

    def insert_after(self, prev_node, val):
        """ Adds a node with value equal to val in the list after prev_node. """
        # Create the new node and insert it into the list
        n = DLL.Node(val=val, nxt=prev_node.next, prev=prev_node)
        
        # Update the chain's pointers
        if prev_node == self.tail:
            self.tail = n
        else:
            prev_node.next.prev = n

        prev_node.next = n

        # Update the size
        self.size += 1

    def delete(self, node):
        """ Removes the specified node from the list. """
        # Update the node's neighbors to remove it from the chain
        if node == self.head:
            self.head = node.next
        else:
            node.prev.next = node.next
        
        if node == self.tail:
            self.tail = node.prev
        else:
            node.next.prev = node.prev

        # Update the internal size
        self.size -= 1

    def index(self, i):
        """
        Returns the node at position i (i<n). Searchs from the most optimal direction
        for the given index.
        """
        if i >= self.size:
            raise IndexError("list index out of range")
        elif i < self.size / 2:
            # If the index is in the front half of the list, just count up to it
            n = self.head
            for j in range(i): n = n.next
        else:
            # If the index if the the second half of the list, count backwards to
            # reduce unnecessary steps
            n = self.tail
            for j in range(self.size - i - 1): n = n.prev
        
        return np

class Queue:
    """
    A doubly-linked list-backed queue implementation.
    """

    def __init__(self):
        """ Initializes the queue using an internal doubly-linked list and list of minimum values. """
        self.internal = DLL()
        self.mval = None
        self.mins = []

    def __len__(self):
        """ Override Python's default len() operation to return a valid result. """
        return len(self.internal)

    def enqueue(self, val):
        """ Pushes the given element onto the beginning of the queue. """
        # dispatch the push operation to the dll
        self.internal.push(val)
        i = -1

        for i in range(len(self.mins) - 1, -1, -1):
            if val >= self.mins[i]:
                break

        # prune the minimum list
        if i != -1: del self.mins[i:]

        # add the new minimum to the list
        self.mins.append(val)

        print(self.mins)

    def dequeue(self):
        """ Removes the last element from the queue in the order of enqueueing. """
        oldest = self.internal.tail
        self.internal.delete(oldest)
        
        # update the minimum list if necessary
        if oldest.val == self.mins[-1]:
            self.mins.pop()

        return oldest.val

    def find_min(self):
        """ Returns the minimum value of the queue. """
        return self.mins[0]


##
## TESTING
##


def test_queue_enqueue():
    """ Performs several enqueue operations and asserts runtime conditions. """
    queue = Queue()
    queue.enqueue(0)
    queue.enqueue(1)
    queue.enqueue(-2)
    queue.enqueue(0)
    queue.enqueue(-2)

    assert len(queue) == 5
    assert queue.find_min() == -2

def test_queue_dequeue_fmin():
    """ Tests the functionality of the dequeue operation in conjunction with find_min function. """
    queue = Queue()
    queue.enqueue(0)
    queue.enqueue(1)
    queue.enqueue(-2)
    queue.enqueue(0)
    queue.enqueue(-2)
    queue.dequeue()
    queue.dequeue()

    assert len(queue) == 3
    assert queue.find_min() == -2

    queue.dequeue()

    assert queue.find_min() == -2
    queue.dequeue()
    assert queue.find_min() == -2
