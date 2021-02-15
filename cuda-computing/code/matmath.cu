/**
 * Contains utility functions for performing simple operations on matrices.
 *
 * @authors: Elias Gabriel, Colin Snow
 **/
#include "matmath.h"

/*
  The GPU kernel (or thread) responsible for calculating a single
	value in the output matrix c. This is replicated for the block grid
  running on the GPU to complete the entire calculation.
 */
__global__ void multkernel(Matrix* a, Matrix* b, Matrix* c) {
	unsigned int row = blockIdx.y * blockDim.y + threadIdx.y;
	unsigned int col = blockIdx.x * blockDim.x + threadIdx.x;
  // holds the intermediate matrix product
	float psum = 0.0;

	// during thread and grid creation it is likely that we needed
  // to round up the number of blocks to a whole number to fit our
  // problemspace. in ceiling the number of blocks, the GPU will
  // execute more threads than we actually need. due to those excess
  // threads, we must ensure that the thread we are currently running
  // is actually within the bounds of our problem and not a throw-away
  //
  // translation: make sure the current thread is actually doing work
	if(row < a->rows && col < b->cols) {
	  // iterate through the row and multiply each element then add it to the total
    for(unsigned int i = 0; i < a->cols; ++i) {
      psum += (a->elements[row*b->cols + i]) * (b->elements[i*b->cols + row]);
	  }
  }

  // store the partial sum in the output matrix
	c->elements[c->cols*row + col] = psum;
}

/*
  Allocates a new block of Unified Memory (URAM) and assigns it to store the
	elements for the provided matrix. URAM is accessible from the CPU and GPU
  and removes the necessity for structure-value copying.
 */
int matmalloc(Matrix** pmat, unsigned int rows, unsigned int cols) {
	cudaError_t err = cudaMallocManaged(pmat, sizeof **pmat);
	if(err != cudaSuccess) {
		fprintf(stderr, "Allocated matrix in URAM: %s\n", cudaGetErrorString(err));
		return EXIT_FAILURE_ALLOC;
	}

  Matrix* mat = *pmat;
  mat->rows = rows;
	mat->cols = cols;

  err = cudaMallocManaged(&mat->elements, rows * cols * sizeof(float));
  if(err != cudaSuccess) {
		fprintf(stderr, "Allocated inner matrix in URAM: %s\n", cudaGetErrorString(err));
		return EXIT_FAILURE_ALLOC;
	}
	
  return EXIT_SUCCESS;
}

/*
  Releases a previously-allocated matrix and it's elements from Unified
  Memory. Future CPU/GPU manipulations to M will SEGFAULT.
 */
int matfree(Matrix* M) { 
  cudaError_t err = cudaFree(M->elements);
  if(err != cudaSuccess || (cudaFree(M) != cudaSuccess)) {
    fprintf(stderr, "Freed matrix from URAM: %s\n", cudaGetErrorString(err));
    return EXIT_FAILURE_FREE;
  }

  return EXIT_SUCCESS;
}

/*
  Multiplies the given matrices A and B. A matrix of sufficient size is
  allocated in Unified Memory (URAM) to store the matrix product and is
  assigned to the pointer chain C.

  NOTES: Reference links to better understand CUDA's execution schema
    - https://stackoverflow.com/a/2392271
    - https://devblogs.nvidia.com/even-easier-introduction-cuda/
    - https://devblogs.nvidia.com/cuda-pro-tip-occupancy-api-simplifies-launch-configuration/
    - https://stackoverflow.com/a/33247118
 */
int matmultiply(Matrix* A, Matrix* B, Matrix** C) {
  // the GPU must spawn threads in multiples of the warp size, which is
  // 32 on all chips to date, so its more efficient to allocate threads
  // of that factor
  //
  // TODO: scale tpb by matrix ratio but maintain multiple of 32 between 128-512
  dim3 threadsPerBlock(16, 16); // lowest square multiple of 32

  // find the minimum number of blocks to fit the data, overfitting if we cannot
  // roundly divide the number of threads to fit our matrix dimensions
  dim3 numBlocks(((*C)->cols + threadsPerBlock.x - 1) / threadsPerBlock.x, ((*C)->rows + threadsPerBlock.y - 1) / threadsPerBlock.y);

	// Run the kernel with the set sizes and the variables a,b,c
	multkernel<<<numBlocks, threadsPerBlock>>>(A, B, *C);

	// wait to synchronize and join all the running CUDA cores
  // this ensures the calculation is completed
	cudaError_t cerr = cudaDeviceSynchronize();
	if(cerr != cudaSuccess) {
		printf("Synchronizing GPU threads: %s\n", cudaGetErrorString(cerr));
		return EXIT_FAILURE_SYNC;
	}

	return EXIT_SUCCESS;
}

/*
   Converts the given matrix to a string represenation and prints
   it to the standard output.
*/
void matprint(Matrix* M) {
  printf("[ ");

  for(unsigned int i = 0; i < M->rows; ++i) {
    for(unsigned int j = 0; j < M->cols; ++j) {
      if(i + j > 0) printf("  ");
      printf("%g ", M->elements[M->cols*i + j]);
    }

    if(i < M->rows - 1) printf("\n");
  }

  printf("]\n");
}
