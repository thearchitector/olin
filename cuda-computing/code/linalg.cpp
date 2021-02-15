//
// Created by Kyle Combes on 3/20/20 for Software Systems at Olin College.
//

#include "linalg.h"
#include <stdio.h>
#include <stdlib.h>
#include <algorithm>
using namespace std;

Kernel *create_kernel(unsigned int width, unsigned int height, float **rows) {
    Kernel *k = (Kernel *)malloc(sizeof(Kernel));
    k->width = width;
    k->height = height;
    k->rows = (float **)malloc(sizeof(float **) * height);
    for (int y = 0; y < height; ++y) {
        k->rows[y] = (float *)malloc(sizeof(float) * width);
        for (int x = 0; x < width; ++x) {
            k->rows[y][x] = rows[y][x];
        }
    }
    return k;
}

/**
 * Gets the value of the kernel at the given position.
 * @param row the y-value in the grid
 * @param col the x-value in the grid
 * @return the value of that position in the kernel
 */
float Kernel::get_component(int row, int col) {
    if (row < 0 || row >= this->height) return 0;
    if (col < 0 || col >= this->width)  return 0;

    return this->rows[row][col];
}

void free_kernel(Kernel *k) {
    for (int i = 0; i < k->height; ++i) {
        free(k->rows[i]);
    }
    free(k->rows);
    free(k);
}

void apply_kernel_to_loc(Image *img, Kernel *k, int numChannels, int row, int col, Image *res) {
    // Allocate memory to read the pixels from the source image into
    unsigned char *readPixel = (unsigned char *)malloc(sizeof(char) * img->channels);
    // Create a temporary place to keep our floating-point math
    float temp[img->channels] = { 0 };
    int horzPad = k->width / 2;
    int vertPad = k->height / 2;
    for (int y = 0; y < k->height; ++y) {
        for (int x = 0; x < k->width; ++x) {
            int py = min(max(row - vertPad + y, 0), (int)img->height-1);
            int px = min(max(col - horzPad + x, 0), (int)img->width-1);
            // Default to 0 (for zero-padding)
            for (int c = 0; c < img->channels; ++c) readPixel[c] = 0;
            // Get the current pixel value, if in bounds (otherwise stays 0)
            img->get_pixel(py, px, readPixel);
            // Get the corresponding kernel component
            float kernelComp = k->get_component(y, x);
            // Apply the kernel to each channel of the src pixel
            for (int c = 0; c < numChannels; ++c) {
                temp[c] += readPixel[c] * kernelComp;
            }
        }
    }
    // Convert the floating-point sums into chars
    unsigned char tempChar[img->channels] = { 0 };
    for (int c = 0; c < numChannels; ++c) {
        tempChar[c] = temp[c];
    }
    res->set_pixel(row, col, tempChar);
}

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
Image *convolve(Image *img, Kernel *k) {
    // Ensure kernel dimensions are odd
    if (k->height % 2 != 1 || k->width % 2 != 1) {
        fprintf(stderr, "Kernel dimensions must be odd, not %dx%d.\n", k->height, k->width);
        return NULL;
    }

    short numChannels = img->channels;
    if (numChannels == 4) { // There's an alpha channel
        // Ignore it
        numChannels = 3;
    }

    // Prepare the result
    Image *res = create_blank_image(img->width, img->height, img->channels);

    // Apply the kernel to the image
    unsigned char *row;
    for (int y = 0; y < img->height; ++y) {
        row = res->rows[y];
        for (int x = 0; x < img->width; ++x) {
            apply_kernel_to_loc(img, k, numChannels, y, x, res);
        }
    }

    // Copy over any channels that weren't convolved
    int channelDiff = img->channels - numChannels;
    for (int i = 0; i < channelDiff; ++i) {
        int c = numChannels + i;
        res->copy_channel(img, c, c);
    }

    return res;
}
