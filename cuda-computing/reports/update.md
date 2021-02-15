# CUDA Computing
Elias Gabriel, Colin Snow, Kyle Combes

> ## Project Goals
> We aim to learn more about GPU computing in the C language, specifically using the [CUDA platform](https://developer.nvidia.com/about-cuda) for parallelized programming. Besides raw implementation, we want to develop an intuition about how GPUs interact with standard proccesses (from a compilation-code perspective and a from a bus-I/O perspective).
>
> ## Learning Goals
> 1. Develop an understanding of the hardware differences between a CPU and a GPU
> 2. Get some experience with CUDA.
> 3. Get a better sense for what GPU computing is good for.
> 4. Learn how to use/practice using structs in C.
> 5. Make a flowchart for CUDA code compilation and execution

## Current Status
We've completed our MVP, which was to have an Google Colabratory environment that can execute pre-packaged CUDA algorithms and perform matrix multiplication. We also learned what CUDA stands: Compute Unified Device Architecture.

Throughout our progress, we've been developing a more solid understanding the GPU programming and execution lifecycle. However, there is still plenty of room for improvment and learning.

We have created a program which can multiply large matrices concurrently and quickly. We've intentionally separated that multiplication program into an independent modules with a fleshed-out and stable API. The idea is that the future work in image processing will be able to use the same code.

We have also successfully loaded a PNG image into a `char **`, inverted the RGB channels of each pixel, and saved the image as a new PNG. This means we can start to do image processing and apply the other parts of our project to them, such as blurring via 2D kernel convolution.

## Next Steps
 - [x] Submit project proposal
 - [x] Get CUDA running with C in Colab
 - [x] Research GPUs and create a hardware block diagram
 - [x] Follow and implement the documented ['Basics'](https://www.nvidia.com/docs/IO/116711/sc11-cuda-c-basics.pdf) CUDA tutorial
 - [x] Learn the basics of structs in C and how they can be applied to GPU computing
 - [x] Load PNG from file into matrix and save matrix to PNG
 - [x] Multiply two matrices and return the correct result
 - [x] Extract the function API to an independent module
 - [ ] Load in a matrix to the multiplier from the command line [elias]
 - [ ] Enable piping raw input from file streams to the multiplier [elias]
 - [ ] Apply kernels to images for convolution [kyle]
 - [ ] Save and load data/matrices to and from CSV [colin]
 - [ ] Unify the Image and Matrix structs [all]
 
 
 ## Links
 GitHub: https://github.com/thearchitector/SoftSysCUDAComputing/edit/master/
 
 Trello: https://trello.com/b/pE8Qo4oN/cudacomputing
