# CUDA Computing
> Elias Gabriel, Colin Snow, Kyle Combes

## Project Goals
We aim to learn more about GPU computing in the C language, specifically using the [CUDA platform](https://developer.nvidia.com/about-cuda) for parallelized programming. Besides raw implementation, we want to develop an intuition about how GPUs interact with standard proccesses (from a compilation-code perspective and a from a bus-I/O perspective).

### Basic model
At minimum, we want to have an environment running that can execute pre-packaged CUDA algorithms on a Google Colabratory GPU. In addition, we hope to have a solid understanding the GPU programming and execution lifecycle.

We will work through the [CUDA C/C++ basics](https://www.nvidia.com/docs/IO/116711/sc11-cuda-c-basics.pdf) presentation/tutorial from NVIDIA. This will walk us through creating a "Hello World" app, adding vectors, and multi-threading.

### Options for extension

1. Matrix multiplication
    * GPUs are very food at performing many small operations, so a natural application of this speed is in performing large amounts of multiplication operations. Matrix multiplication is the base of many other operations, so doing it quickly can have a wide range of applications.
    * Specifically, we're going to try and implement a CLI for fast matrix multiplication.
2. Image rendering
    * As GPUs are very efficient at matrix multiplication, they are primarily used for graphics processing. Performing many pixel and color operations at once, they are ideal for things like image blurring, dithering, and color correction.
    * Specifically, we're going to implement a program that accepts an image as an input, performs a simple manipulation, and then saves it again.
 
## Learning Goals

1. Develop an understanding of the hardware differences between a CPU and a GPU
2. Get some experience with CUDA.
3. Get a better sense for what GPU computing is good for.
4. Learn how to use/practice using structs in C.
5. Make a flowchart for CUDA code compilation and execution

## Getting Started
We are planning on trying to use CoLab to start because they have built-in CUDA support and we do not need to spend any time setting up environments. Our first objective is to get something working with CUDA, then we will expand to specific applications.


## Next Steps

1. ~~Submit project proposal~~
2. Update Trello board with discretized tasks for our subprojects
3. Get CUDA running with C in Colab
4. Research GPUs and create a hardware block diagram
5. Follow and implement the documented ['Basics'](https://www.nvidia.com/docs/IO/116711/sc11-cuda-c-basics.pdf) CUDA tutorial
6. Learn the basics of structs in C and how they can be applied to GPU computing
