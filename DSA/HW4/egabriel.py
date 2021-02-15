"""
Solves the Maximum Consecutive Subarray problem using a divide and conquer method.

@author: Elias Gabriel
"""
import numpy as np

def brange(scores, start, end):
    if start == end: return start, end, scores[start]
    
    # get the middle index (clamped to int)
    mid = (start + end) // 2

    # set the initial best array to -inf to ensure we get _something_
    lbest = rbest = float('-inf')
    lsum = rsum = 0
    # just use dummy values for now
    lrange = None
    rrange = None

    # start at the middle and work left to the start to get the best array
    for i in range(mid, start - 1, -1):
        lsum += scores[i]
        
        if lsum > lbest:
            lbest = lsum
            lrange = i, mid

    # start at the middle and work right to the end to get the best array
    for i in range(mid + 1, end + 1):
        rsum += scores[i]

        if rsum > rbest:
            rbest = rsum
            rrange = mid, i

    # the best subarray can exist in 3 places. in the first and last cases, we can
    # find the best sum by recursively calling this method
    # 
    # 1) fully on the left of the middle
    a = brange(scores, start, mid)
    # 2) fully on the right of the middle
    c = brange(scores, mid + 1, end)
    # 3) or across the middle
    b = lbest + rbest

    # compare the best values for all the cases and get the maximum one
    # return the sum and the array so we can keep track of indicies and values
    if a[2] > b and a[2] > c[2]:
        return start, mid + 1, a[2]
    elif b >= c[2]:
        return lrange[0], rrange[1] + 1, b
    else:
        return mid, end + 1, c[2]


##
## TESTING
##


def test_brange():
    """
    Tests the calculated optimal subsequence and sum against a known
    optimal range.
    """
    foods = ["french fries", "brussel sprouts", "chicken sandwiches", "tomato soup", "fruit salad"]
    scores = [2, 10, 3, -1, 7]
    meal = brange(scores, 0, 4)

    assert meal[2] == 21
    assert meal[0] == 0
    assert meal[1] == 5

    scores = [2, -9, 4, 2, 5, 3]
    meal = brange(scores, 0, 5)

    assert meal[2] == 14
    assert meal[0] == 2
    assert meal[1] == 6


##
## EXPERIMENTATION
##


def draw_uniform():
    """
    Calculates the average subsequence sum and length across n trials of a uniform distribution
    of numbers in the range [-10, 10].
    """
    s = np.random.randint(-10, 10, size=(100, 100))
    asize = 0
    ahapp = 0

    for h in s:
        meal = brange(h, 0, len(h) - 1)
        asize += meal[1] - meal[0]
        ahapp += meal[2]

    print("Uniform distribution:")
    print(" --> average size:", asize / 100)
    print(" --> average score:", ahapp / 100)

def draw_weighted():
    """
    Calculates the average subsequence sum and length across n trials of a weighted Gaussian
    distribution of numbers in the range [-10, 10].
    """
    # generate all the random distributions
    ps = np.random.random(100)
    hs = np.random.randn(100, 100)
    asize = 0
    ahapp = 0

    for i, p in enumerate(ps):
        # conditionally adjust our distribution mu and sigma values
        if p < 0.7:
            h = 1 * hs[i] + 6
        
        if p >= 0.7:
            h = 0.5 * hs[i] - 7

        meal = brange(h, 0, len(h) - 1)
        asize += meal[1] - meal[0]
        ahapp += meal[2]

    print("Weighted distribution:")
    print(" --> average size:", asize / 100)
    print(" --> average score:", ahapp / 100)


if __name__ == "__main__":
    draw_uniform()
    print()
    draw_weighted()
