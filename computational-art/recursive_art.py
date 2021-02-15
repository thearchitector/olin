"""
A set of tools for looking at art from a computer's perspective.

@author: Elias Gabriel
@revision: v2.0
"""
import random
from PIL import Image
from numpy import pi, cos, sin, tanh, sinh, cosh, arctan, linspace
from itertools import product
# Use the uqfoundation/multiprocess package to support lambda pickling, since
# the default package does not support it.
# Required to send the result of `build_random_function()` to multiple processes.
import multiprocess as mp



###
### BEGIN PATCH
###



# Define global functions to use when mapping pixels, accepts tuple (x, y)
FUNCTIONS = [
    lambda c: c[0] * c[1],
    lambda c: (c[0] + c[1]) / 2,
    lambda c: cos(pi * c[0]),
    lambda c: cos(pi * c[1]),
    lambda c: sin(pi * c[0]),
    lambda c: sin(pi * c[1]),
    lambda c: c[0],
    lambda c: c[1],
    lambda c: tanh(c[0]),
    lambda c: tanh(c[1])
]


def build_random_function(min_depth, max_depth):
    """ Builds a random function of depth at least min_depth and depth at most max_depth.

    - min_depth: the minimum depth of the random function
    - max_depth: the maximum depth of the random function

    # Set random seed to generate same number every time (ensures doctest passes).
    # Run doctests of the function with varying parameters.
    # All of the doctests are testing the depth requirements. We want to verify that the
      function behaviors correctly. 
    : The first test checks an expected depth range and coordinate pair.
    : The second and third checks test that the outputs are the same. They should be
      the same since the third check's minimum value should be clamped up to 1 from -1.
      Before the second and third tests we reset the random seed to ensure the outputs
      are the same again.
    : The fourth test checks normal behavior again, with a negative in the coordinate pair.
    : The fifth test makes sure the function throws an error if the minimum depth is
      less than the maximum value, as this is a logial requirements.
    >>> random.seed(4558106513883317379)
    >>> build_random_function(3, 5)((0.25, 0.75))
    0.4632169206037787
    >>> random.seed(4558106513883317379)
    >>> build_random_function(1, 9)((-1, 1))
    -0.8807970779778824
    >>> random.seed(4558106513883317379)
    >>> build_random_function(-1, 9)((-1, 1))
    -0.8807970779778824
    >>> build_random_function(2, 7)((0.42, -0.873))
    -0.606202227848691
    >>> build_random_function(4, 3)((0, 0))
    Traceback (most recent call last):
        ...
    Exception: The minimum depth must be less than the maxiumum!
    """
    # Throw an error if the min is greater than the max because that's not allowed!
    if min_depth > max_depth:
        raise Exception("The minimum depth must be less than the maxiumum!")

    # Clamp the depths to a minimum of 1, as depths less that 1 are not possible to generate.
    min_depth = max(1, min_depth)
    max_depth = max(1, max_depth)

    # Choose a random function from the list of possibilities
    rand_func = random.choice(FUNCTIONS)

    # If we haven't reached the maximum depth, and haven't reached the minimum depth OR
    # if we have reached the minimum depth and randomly decide to keep going
    if max_depth > 1 and (min_depth > 1 or random.random() >= 0.5):
        # Generate random function chain for the x value, decreases the min and max to respect depths
        x_func = build_random_function(min_depth - 1, max_depth - 1)
        # Do same as above for the y value
        y_func = build_random_function(min_depth - 1, max_depth - 1)
        # Return a lambda function calling the random function with the function chains as a tuple arg
        return lambda c: rand_func((x_func(c), y_func(c)))
    
    # Retuen a lambda function calling the random function
    return lambda c: rand_func(c)


def remap_interval(val, min1, max1, min2, max2):
    """ Remap a value from one range to a new range.

    - val: the value to remap
    - min1: the minimum for the old range `val` is within
    - max1: the maximum for the old range `val` is within
    - min2: the minimum for the new range
    - max2: the maximum for the new range
    
    # The doctests in this functiona originally were nearly sufficient, as they tested
      several numbers at different intervals.
    : I added an additional unit test to check that the remap function works with negative numbers,
      as it would need to remap values from -1 to 1, to 0 to 255.
    >>> remap_interval(0.5, 0, 1, 0, 10)
    5.0
    >>> remap_interval(5, 4, 6, 0, 2)
    1.0
    >>> remap_interval(5, 4, 6, 1, 2)
    1.5
    >>> remap_interval(0, -1, 1, 0, 255)
    127.5
    """
    # Take the value and remove the previous minimum, then multiply by the difference
    # raitio, and then add the new minimum 
    return (((max2 - min2) / (max1 - min1)) * (val - min1)) + min2


def color_map(val):
    """ Maps input value between -1 and 1 to an integer 0-255, suitable for use as an RGB color code.
 
    - val: value to remap, must be a float in the interval [-1, 1]

    : I felt that the default unit tested provided were sufficient to test the functionality
      of the color map function. The unit tests check a wide range of possible values, from the
      miniumum to the maxiumum value the function should handle.
    >>> color_map(-1.0)
    0
    >>> color_map(1.0)
    255
    >>> color_map(0.0)
    128
    >>> color_map(0.5)
    191
    """
    # Nested round within integer cast to round rather than floor, makes nicer color range
    return int(round(remap_interval(val, -1, 1, 0, 255)))


def generate_art(filename, x_size=350, y_size=350):
    """ Generates computational art and saves as an image. Automatically determines if job should be
    run on multiple or a single core based image size and available processors. Wraps `*_sync` and
    `*_async`, but exists for compatability with base code.

    # Unit tests wouldn't be very helpful with this function, as it outputs a file.
    """
    # If image is less than 4096 pixels or there is only 1 available core, run on a single core.
    # Threshold determined experimentally.
    if x_size * y_size < 64**2 or mp.cpu_count() < 2:
        generate_art_sync(filename, x_size, y_size)
    else:
        generate_art_async(filename, x_size, y_size)


def generate_art_sync(filename, x_size, y_size):
    """ Generate computational art and save as an image file.

    - filename: string filename for image (should be .png)
    - x_size, y_size: dimensions of image

    # Unit tests wouldn't be very helpful with this function, same as above.
    """
    # Functions for red, green, and blue channels - where the magic happens!
    red_function = build_random_function(9, 20)
    green_function = build_random_function(9, 20)
    blue_function = build_random_function(9, 20)
    
    # Create image and loop over all pixels
    im = Image.new("RGB", (x_size, y_size))
    pixels = im.load()
    
    for i in range(x_size):
        for j in range(y_size):
            x = remap_interval(i, 0, x_size, -1, 1)
            y = remap_interval(j, 0, y_size, -1, 1)
            c = (x, y)
            pixels[i, j] = (
                color_map(red_function(c)),
                color_map(green_function(c)),
                color_map(blue_function(c))
            )

    im.save(filename)


def generate_art_async(filename, x_size, y_size):
    """ Generate computational art with a worker pool and save as an image file.

    - filename: string filename for image (should be .png)
    - x_size, y_size: dimensions of the image
    
    # Unit tests wouldn't be very helpful with this function, same as above.
    """
    # Functions for red, green, and blue channels - where the magic happens!
    red_function = build_random_function(9, 15)
    green_function = build_random_function(9, 15)
    blue_function = build_random_function(9, 15)
    
    # Create image of given size with RGB colorspace
    im = Image.new("RGB", (x_size, y_size))
    
    # Define range of coordinates to pass to color functions.
    # Cartesian product two ranges of values from -1 to 1 of [x/y]_size.
    # This is equivilent to a nested for loop of range(size) with inner remap_interval call
    # (see `generate_art_sync` for comparison).
    coordinates = list(product(linspace(-1, 1, num=x_size), linspace(-1, 1, num=y_size)))

    # Create a worker pool, using all cores because we're not nice
    pool = mp.Pool(mp.cpu_count())
 
    # Split up all the color computations by sending them to the worker pool.
    # Each job runs the specificed color function with one coordinate pair from the list.
    reds = pool.map_async(red_function, coordinates)
    greens = pool.map_async(green_function, coordinates)
    blues = pool.map_async(blue_function, coordinates)

    # Zip together the individual values into a list of RGB tuples (r, g, b)
    pixels = list(zip(
        map(color_map, reds.get()),
        map(color_map, greens.get()),
        map(color_map, blues.get())
     ))

    # Close and resync the worker pool with the main process
    pool.close()
    pool.join()

    # Set the image data to the new pixels and save
    im.putdata(pixels)
    im.save(filename)



###
### END PATCH
###



if __name__ == '__main__':
    # Run doctests
    #import doctest
    #doctest.testmod()
    
    # Time generation functions to determine threshold => 64x64
    # I ran the code with different sizes to determine at what image size multiprocessing
    # would be actually useful. Sending jobs to a worker pool incurs a cost, and the speedup
    # is only helpful when the number of processed pixels exceeds the threshold.
    # With the default values, multiprocessing the process sped up generation by ~3x, which makes
    # sense given that I separated the 3 different color channels and processed them in parallel.
    #
    # >>> python recursive_art.py 
    # 205.28423964200192      (multi)
    # 660.2333436690024       (single)
    #
    #import timeit
    #print(timeit.timeit("generate_art_async('art_test.png', 350, 350)", number=10, setup="from __main__ import generate_art_async; import random; random.seed(4558106513883317379)"))
    #print(timeit.timeit("generate_art_sync('art_test2.png', 350, 350)", number=10, setup="from __main__ import generate_art_sync; import random; random.seed(4558106513883317379)"))
    
    # Prompt the user for filenames and image dimensions, and print the runtiem for fun
    import time
    filename = input('[Recursive Art] How would you like to write your image (filename.png)? ')
    width = int(input('[Recursive Art] What width of image would you like to generate? '))
    height = int(input('[Recursive Art] What should its height be? '))
    base = time.time()
    print("\n==============\n")

    generate_art(filename, width, height)
    print("Time to generate:", time.time() - base, "seconds\n")
