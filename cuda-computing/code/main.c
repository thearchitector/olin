#include "matmath.h"

void fillRandom(Matrix* m) {
	for(unsigned int i = 0; i < m->rows; ++i) {
		for(unsigned int j = 0; j < m->cols; ++j) {
		  m->elements[m->rows*j + i] = 1.0;//(float)rand() / (float)RAND_MAX;
	  }
	}
}

int main(int argc, char* argv[]) {
  int r1, c1, r2, c2;
  r1 = c2 = 3;
  r2 = c1 = 3;

  if(r1 != c2) {
    fprintf(stderr, "Incompatable matrix dimensions!");
    return EXIT_FAILURE_DIMS;
  }

	Matrix* A;
  Matrix* B;
  Matrix* C;

  int err = matmalloc(&A, r1, c1);
  if(err != EXIT_SUCCESS) return err;
  err = matmalloc(&B, r2, c2);
  if(err != EXIT_SUCCESS) return err;
  err = matmalloc(&C, r1, c2);
  if(err != EXIT_SUCCESS) return err;

  fillRandom(A);
  fillRandom(B);

	if(matmultiply(A, B, &C) != EXIT_SUCCESS) return EXIT_FAILURE;

  printf("\n");
  matprint(A);
  printf("\n");

  printf("\n");
  matprint(B);
  printf("\n");

  printf("\n");
  matprint(C);
  printf("\n");

  err = matfree(A) != EXIT_SUCCESS ? 1 : 0;
  err += matfree(B) != EXIT_SUCCESS ? 1 : 0;
  err += matfree(C) != EXIT_SUCCESS ? 1 : 0;
  return err > 0 ? EXIT_FAILURE : EXIT_SUCCESS;
}  
