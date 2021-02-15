"""
    An example of dynamic programming - wildcard string matching.

    @author: Elias Gabriel
"""
import string
from hypothesis import given
from hypothesis.strategies import from_regex

def match(strn, pattern):
    """ Checks whether the given string can be matched using the provided pattern. """
    # create a lookup matrix
    B = [[False for j in range(len(pattern) + 1)] for i in range(len(strn) + 1)]

    # base case #1: empty string and pattern
    B[0][0] = True

    # base case #2: empty string
    ## if the string is empty then the pattern can only contain wildcards
    for j, c2 in enumerate(pattern, 1):
        # if c2 is ever calm, just stop early
        if c2 == '*': B[0][j] = B[0][j - 1]
        else: break

    # base case #3: empty pattern
    ## if the pattern is empty the string must be empty
    ## do nothing because they're already false

    # do the tabulation, bottom-up, with start at (1, 1)
    for i, c1 in enumerate(strn, 1):
        for j, c2 in enumerate(pattern, 1):
            # if the characters match, skip it
            if c1 == c2: B[i][j] = B[i - 1][j - 1]
            # if there is a wildcard, there are two options:    
            #   - the wildcard is matching nothing
            #   - the wildcard is matching something
            elif c2 == '*': B[i][j] = (B[i][j - 1] or B[i - 1][j])
            # no wildcard, no match, no service
            else: B[i][j] = False

    # if the strings match, then the truthiness should have propagated upward
    return B[-1][-1]


##
## TESTING
##


@given(from_regex(r"\A[a-z]*e\Z"))
def test_match_front(s):
    """
    Checks for that strings following `{any number of letters}e` fit the pattern `*e`. This tests
    for random strings appended by a matching character.
    """
    assert match(s, "*e")
    assert not match(s, "*a")

@given(from_regex(r"\As[a-z]*e\Z"))
def test_match_center(s):
    """
    Checks for that strings following `s{any number of letters}e` fit the pattern `s*e`. This tests
    for random string padded with matching characters.
    """
    assert match(s, "s*e")
    assert not match(s, "p*e")

@given(from_regex(r"\As[a-z]*\Z"))
def test_match_back(s):
    """
    Checks for that strings following `s{any number of letters}` fit the pattern `s*`. This tests
    for random strings prepended by matching characters.
    """
    assert match(s, "s*")
    assert not match(s, "p*")

@given(from_regex(r"\A\**\Z"))
def test_match_empty(s):
    """ Checks that any length of wildcards (including 0) matches an empty string. """
    assert match("", s)

@given(from_regex(r"\A\*+\Z"))
def test_match_redundant(s):
    """
    Checks that any length of wildcards (excluding 0) can be collapsed into a single character.
    This effectively tests the opposite behavior as `test_match_sweeping`.
    """
    assert match("a", s)

@given(from_regex(r"\A\[a-z]*\Z"))
def test_match_sweeping(s):
    """
    Checks that a single wildcard can match any string (including blank). This effectivly
    tests the opposite behavior to that tested by `test_match_redundant`.
    """
    assert match(s, "*")
