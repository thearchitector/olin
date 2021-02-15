/**
 * The public-facing API for creating and manipulating matrices.
 *
 * @author: Elias Gabriel, Colin Snow
 **/
#ifdef __cplusplus
extern "C" {
#endif

#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include "codes.h"

typedef struct {
  unsigned int rows;
	unsigned int cols;
  float* elements;
} Matrix;

int matmalloc(Matrix**, unsigned int, unsigned int);
int matmultiply(Matrix*, Matrix*, Matrix**);
int matfree(Matrix*);
void matprint(Matrix*);

#ifdef __cplusplus
}
#endif
