"""
Provides functionality for finding and returning the longest subsequence of consecutive
increasing integers in a given list.

@author: Elias Gabriel
@revision: v1.0.1
"""

# NOTE: In terms of implementation, this function tracks sequences by their indices in the master
# list rather than keeping track of the subsequences themselves. This is to avoid the use of
# list operations like `extend`, which are linear in O(k) and would result in an overall worst-case
# complexity of O(n^2) rather than O(n).
def findLongestSubstring(a):
    """ Finds and returns the longest consecutive subsequence of integers in the provided list. """
    lsidx = leidx = csidx = ceidx = 0

    # Loop through all the elements in the list with their indices
    for i, n in enumerate(a):
        # Check if the current number is higher than the last
        if i == 0 or n > a[i-1]:
            # Increase the candidate range to include the new number
            ceidx += 1

            # If the current candidate length is greater than the known max, set
            # the new maximum
            if ceidx - csidx > leidx - lsidx:
                lsidx = csidx
                leidx = ceidx
        else:
            # Set the new candidate index range
            csidx = i
            ceidx = i + 1

            # Early stop condition. If the longest subsequence we've found is longer than
            # or equal to the number of remaining ints, we know that we don't have to
            # keep looking.
            if leidx - lsidx >= len(a) - i:
                break

    return a[lsidx:leidx]

def test_findLongestSubstring():
    """ A unit test for various inputs and cases for the above function. """
    assert findLongestSubstring([]) == []
    assert findLongestSubstring([9, 8, 7, 6, 5, 4, 3, 2, 1]) == [9]
    assert findLongestSubstring([1, 2, 3, 4, 5, 6, 7, 8, 9]) == [1, 2, 3, 4, 5, 6, 7, 8, 9]

    assert findLongestSubstring([1, 2, 0, 4, 8, 9, 3]) == [0, 4, 8, 9]
    assert findLongestSubstring([1, 2, 3, 4, 0, 1, -1, 2, 4, 5, 6, 7, 8, 5]) == [-1, 2, 4, 5, 6, 7, 8]
    assert findLongestSubstring([7, 4, 8, 2, 6, 9, 1, 3]) == [2, 6, 9]
