//
// Created by Kyle Combes on 3/20/20 for Software Systems at Olin College.
//

#include "img.h"

struct Kernel {
    unsigned int width;
    unsigned int height;
    float **rows;

    /**
     * Gets the value of the kernel at the given position.
     * @param row the y-value in the grid
     * @param col the x-value in the grid
     * @return the value of that position in the kernel
     */
    float get_component(int row, int col);
};

/**
 * Convolves an image with a kernel. Edges are extended (i.e. when applying a
 * 3x3 kernel to pixel (0, 0), "pixels" (-1, -1), (0, -1) and (-1, 0) are
 * assumed to be identical to pixel (0, 0). Therefore, the resulting image will
 * have the same resolution as the source image.
 * @param img the image to convolve with the kernel
 * @param k the kernel to convolve with the image
 * @return the resulting image (with the same dimensions and alpha channel as
 * the source)
 */
Image *convolve(Image *img, Kernel *k);
Kernel *create_kernel(unsigned int width, unsigned int height, float **rows);
void free_kernel(Kernel *k);
