# Basic Matrix Operations Using CUDA (With a Side of Image Convolution)

By Elias Gabriel, Colin Snow, and Kyle Combes for [Software Systems](https://sites.google.com/site/softsys20/home) at Olin College of Engineering

## Project Goals
At the outset, we wanted to learn more about GPU computing in C/C++, specifically using NVIDIA's [CUDA platform](https://developer.nvidia.com/about-cuda) for parallelized programming. This morphed into a desire to implement some basic linear algebra computation, including adding and multiplying matrices on a GPU. We then wanted to use that to convolve matrices so that we could apply various kernels/filters to images.

## Learning Goals
1. Develop an understanding of the hardware differences between a CPU and a GPU
2. Get some experience with CUDA
3. Get a better sense for what GPU computing is good for
4. Learn how to use/practice using structs in C
5. Make a flowchart for CUDA code compilation and execution

### Progress on Goals
We achieved all of our learning goals except number 5, which still continues to confuse us a little. We managed to go well beyond our minimum product and produce multiple different components which function independently and perform different operations. In doing this, each of us got exposed to CUDA and the benefits/drawbacks of parallel computing.

## What We Created
We created a program which can multiply large matrices concurrently and quickly (sometimes getting correct results). We've intentionally separated that multiplication program into an independent modules with a fleshed-out and stable API. We learned more about how to allocate and deal with structures in CUDA-C, and took advantage of nifty memory management techniques we learned about in the text resources we found.

```sh
    $ ./mmulrand

    input_1 = [ 1   1   1 
                1   1   1 
                1   1   1 ]

    input_2 = [ 1   1   1 
                1   1   1 
                1   1   1 ]

    answer = [ 3   3   3 
               3   3   3 
               3   3   3 ]
```

We also implemented image convolution in C++, but doing so took longer than expected and thus we were unable to port the code to CUDA within the timeframe of the project. We were able to apply a blurring filter to some PNGs though:

![Blurred minions](https://imgur.com/4gKo2mH.png)


## Running the Code

### Matrix Multiplication
> _Requires CUDA version 10.2 (which should be installed at `/opt/cuda`)_
> _Not all NVIDIA GPUs support CUDA 10.2_
> _If you choose to install CUDA, you must restart your computer before running this program. Please be aware this can break your system if not done correctly; the installation process is different depending on your Linux distribution._

```bash
    $ make mmulrand
    $ ./mmulrand
```

### Image Blurring

You can try blurring your own PNG images by compiling the code and running `convolve_test`, like so:

```bash
    $ make convolve_test
    $ ./convolve_test <path_to_src_img> <path_to_output_img>
```

(If the image comes out weird, make sure the source image is in the RGB or RGBA format.)

To change the kernel being convolved with the image, simply edit lines 13-15 in `convolve_test.cpp` and re-run `make`. (Do note that the dimensions of the kernel must be odd.)

## Reflection
The project was a success in terms of exposing us to computing with CUDA. We also gained practice with object-oriented programming in C++, including writing and using `struct` member functions.

It would have been nice to get the image convolution working on the GPU, but it was still satisfying to get it working on the CPU.

Separately, we struggled with achieving our 5th learning goal for a couple of reasons. Primarily, the method in which CUDA actually executes codes is really complicated and, from what we can tell, fairly unpredictable if written incorrectly. From a software side, that made it really challenging to debug and understand what was going on behind the scenes. Secondly, the resources we did find explaning how execution worked were not extremely extensive, nor did many of them explain things in layman's terms.

All combined we didn't get the application working perfectly, which is something we were hoping to achieve. Depending on the matrix size and the numbers within it, the product we got was correct only some of the time and without clear reasons. Given more time, we think that more of our early-time should have been spent trying to better un3derstand the hardware-side of GPUs so that we could have a better understanding of its implications on our software.

## Helpful Learing Resources

The [CUDA C/C++ Basics](https://www.nvidia.com/docs/IO/116711/sc11-cuda-c-basics.pdf) PDF from NVIDIA gave us a good intro to programming with CUDA. It helped us write our first "Hello World" CUDA app.

In attempt to better understand the execution flow behind CUDA and how it affects programming design decisions, we found a couple of resources:
- **Overview of Architecture and Execution:**
    - [An Even Easier Introduction to CUDA](https://devblogs.nvidia.com/even-easier-introduction-cuda/)
    - [CUDA C Programming Guide (Programming Model)](https://docs.nvidia.com/cuda/cuda-c-programming-guide/index.html#programming-model)
- **Explanations of Implications of Programming Decisions (Threadblocks, Blockgrids, and Warps):**
    - [What the heck are threads, blocks, and warps?](https://stackoverflow.com/a/33247118)
    - [Selecting grid paramaters, an example](https://stackoverflow.com/a/2392271)
    - [Why your parameters are important](https://devblogs.nvidia.com/cuda-pro-tip-occupancy-api-simplifies-launch-configuration/)
- **Tips and Tricks on Writing Good CUDA Code:**
    - https://docs.nvidia.com/cuda/cuda-c-best-practices-guide/index.html
