"""
A minimum heap implementation with <= nlog(n) function times.

@author: Elias Gabriel
"""
import pytest
from hypothesis import given
import hypothesis.strategies as st

class Heap:
	def __init__(self, oglist=None, inplace=True):
		"""
		Initializes a heap from a list of arbitrary length, building it using
		Floyd's algorithm from the bottom leaves to the root in O(n) time. The
		heap uses a the provided list as its internal storage and simply wraps
		it in-place.
		"""
		# if we don't want to reference the oglist, then copy it instead
		self.internal = (oglist if inplace or not oglist else oglist.copy()) or []

		if len(self.internal) > 0:	
			for i in range(len(self.internal) - 1, -1, -1):
				self.heapify(i)
		
	def heapify(self, i):
		"""
		Recursivly fixes the heap-ordering property by comparing left and right
		children to their parents and swapping where necessary.
		"""
		# get left and right child elements
		left = (2 * i) + 1
		right = left + 1
		smallest = i
		A = self.internal

		# get the smallest child if it exists
		if left < len(A) and A[left] < A[i]:
			smallest = left
		if right < len(A) and A[right] < A[smallest]:
			smallest = right

		# if a child is smaller, swap them and run this whole thing again
		if smallest != i:
			A[i], A[smallest] = A[smallest], A[i]
			self.heapify(smallest)

	def __len__(self):
		"""
		Overrides the len(A) function and returns the length of the internal list.
		"""
		return len(self.internal)

	def insert(self, value):
		"""
		Inserts a value into the heap while maintaining the ordered and complete
		heap properties. Insertion happens in log(n) time.
		"""
		self.internal.append(value)
		# the current index is the last element in the array (the bottom-most right)
		k = len(self) - 1

		# while the current index isn't the root
		while k > 0:
			# get the parent element
			parent = (k - 1) // 2

			# if the node at k is less than it's parent
			if self.internal[k] < self.internal[parent]:
				# swap the elements and set the new current
				self.internal[k], self.internal[parent] = self.internal[parent], self.internal[k]
				k = parent
			else:
				# validation was successful, so we know we're done
				return None

	def delete_min(self):
		"""
		Removes the minimum value, or root, from the heap and returns it. The
		heap properties are maintained in log(n) time.
		"""
		# only heapify if we need to (more than 1 element)
		if len(self) > 1:
			# store the current minimum and pop the last element and store it as the root
			m, self.internal[0] = self.internal[0], self.internal.pop()
			# reheapify at the root (which will always cascade to the right)
			self.heapify(0)
			return m
		elif len(self) == 1:
			# if there's just a one element, just pop it
			return self.internal.pop()

		return None

	def min(self):
		"""
		Returns the minimum value (root) of the heap without removing it
		from the heap. Overrides the min(A) function.
		"""
		# if we don't have an element, we don't have a minimum
		return self.internal[0] if len(self) > 0 else None

	def to_sorted(self, reverse=False, inplace=True):
		"""
		Returns a sorted list, either in decreasing or increasing order, of
		all the elements in the heap.
		"""
		if len(self) > 0:
			slist = [None] * len(self)
			length = len(self)
			# if we don't want to modify the heap, copy it first
			h = self if inplace else Heap(self.internal)

			# iteratively remove the minimum element and add it to a list
			for n in range(length):
				i = length - 1 - n if reverse else n
				slist[i] = h.delete_min()

			return slist
		
		return []


##
## TESTING
##


@given(st.lists(st.integers()))
def test_heap_len(l):
	h = Heap(l)
	# compare the list length to the heap length
	assert len(l) == len(h)

@given(st.lists(st.integers()))
def test_heap_minimum(l):
	h = Heap(l)
	# compare the heap's minimum to the list's minimum
	if len(l): assert h.min() == min(l)

@given(st.lists(st.integers()))
def test_heap_insert_delete(l):
	h = Heap()
	l_sorted = sorted(l, reverse=True)
	assert len(h) == 0
	
	# insert the elements in `l` and assert the length changes each time
	for n, i in enumerate(l):
		h.insert(i)
		assert len(h) == n + 1

	# count from the end and iteratively delete the min, asserting that
	# the length has changed each time
	for n in range(len(l) - 1, -1, -1):
		assert h.delete_min() == l_sorted[n]
		assert len(h) == n

@given(st.lists(st.integers()))
def test_heap_delete(l):
	h = Heap(l)
	l_sorted = sorted(l, reverse=True)
	assert len(h) == len(l)
	
	# count down from the length of the list and iteratively delete the min
	for n in range(len(l) - 1, -1, -1):
		assert h.delete_min() == l_sorted[n]
		assert len(h) == n

@given(st.lists(st.integers()))
def test_heapsort(l):
	h = Heap(l, inplace=False)
	lsorted = sorted(l)
	# compare the sorted list to the sorted heap
	assert lsorted == h.to_sorted()
	
	h2 = Heap(l, inplace=False)
	# compare the reversed sorted list and heap
	lsorted2 = sorted(l, reverse=True)
	assert lsorted2 == h2.to_sorted(reverse=True)
