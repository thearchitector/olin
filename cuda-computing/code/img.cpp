/**
 * Loads PNG images into matrices and saves matrices as PNG images.
 *
 * Based on https://gist.github.com/niw/5963798.
 *
 * Requires libpng.
 *
 * Created by Kyle Combes for Software Systems SP20 at Olin College of
 * Engineering.
 */

#include <stdlib.h>
#include <stdio.h>
#include <png.h>
#include "img.h"

/**
 * Copies over the data from the specified channel of the source image.
 * @param src the image to copy data from
 * @param srcChannel the index of the channel to copy data from in the source
 *  image
 * @param destChannel the index of the channel to copy the data to
 * @return false if the dimensions in the two images don't match
 *  or if the channel indexes are out of range of their respective images,
 *  true otherwise
 */
bool Image::copy_channel(Image *src, int srcChannel, int destChannel) {
    if (src->height != this->height || src->width != this->width)
        return false;
    if (srcChannel >= src->channels || destChannel >= this->channels)
        return false;

    int srcColIdx;
    int destColIdx;
    for (int y = 0; y < this->height; ++y) {
        for (int x = 0; x < this->width; ++x) {
            srcColIdx = x*this->channels + srcChannel;
            destColIdx = x*this->channels + destChannel;
            this->rows[y][destColIdx] = src->rows[y][srcColIdx];
        }
    }
    return true;
}

/**
 * Attempts to set the value of a pixel.
 * @param row the row (or y-coordinate) of the pixel
 * @param col the column (or x-coordinate) of the pixel
 * @param val the new value to set the pixel to (between 0 and 255, inclusive).
 *   If the image consists of more than one channel, then val should be an array
 *   of unsigned chars with the same length as the number of channels in the image.
 * @return true if row and col are within the bounds of the image, false otherwise
 */
bool Image::set_pixel(unsigned int row, unsigned int col, unsigned char *val) {
    if (row >= this->height) return false;
    if (col >= this->width)  return false;

    unsigned char *r = this->rows[row];
    int baseIdx = col * this->channels;
    for (int c = 0; c < this->channels; ++c) {
        r[baseIdx + c] = val[c];
    }
    return true;
}

/**
 * Attempts to get the value of a pixel.
 * @param row the row (or y-coordinate) of the pixel
 * @param col the column (or x-coordinate) of the pixel
 * @param res where to put the result (should be of size char times the number
 *   of channels in the image)
 * @return true if row and col are within the bounds of the image, false otherwise
 */
bool Image::get_pixel(int row, int col, unsigned char *res) {
    if (row < 0 || row >= this->height) return false;
    if (col < 0 || col >= this->width)  return false;

    unsigned char *r = this->rows[row];
    int baseIdx = col * this->channels;
    for (int c = 0; c < this->channels; ++c) {
        res[c] = r[baseIdx + c];
    }
    return true;
}

/**
 * Prints out a grid of pixel values for each channel.
 */
void Image::print_channels() {
    unsigned char *px = (unsigned char *)malloc(sizeof(char) * this->channels);
    for (int c = 0; c < this->channels; ++c) {
        printf("Channel %d:\n", c);
        for(int y = 0; y < this->height; y++) {
            for (int x = 0; x < this->width; x++) {
                if (!this->get_pixel(y, x, px)) return;
                printf("%3d ", px[c]);
            }
            printf("\n");
        }
        printf("\n");
    }
}

/**
 * Creates a new blank image with all pixels and all channels set to 0.
 * @param width the width of the image
 * @param height the height of the image
 * @param channels the number of channels for each pixel
 * @return a new Image
 */
Image *create_blank_image(unsigned int width, unsigned int height, unsigned int channels) {
    Image *res = (Image *)malloc(sizeof(Image));
    res->height = height;
    res->width = width;
    res->channels = channels;
    unsigned char **rows = (unsigned char **)malloc(sizeof(char *) * height);
    for (int y = 0; y < height; ++y) {
        rows[y] = (unsigned char *)calloc(width * channels, sizeof(char));
    }
    res->rows = rows;
    return res;
}

Image *read_png_file(char *filename) {
    FILE *fp = fopen(filename, "rb");

    png_structp png = png_create_read_struct(PNG_LIBPNG_VER_STRING, NULL, NULL, NULL);
    if(!png) abort();

    png_infop info = png_create_info_struct(png);
    if(!info) abort();

    if(setjmp(png_jmpbuf(png))) abort();

    png_init_io(png, fp);

    png_read_info(png, info);

    png_byte color_type = png_get_color_type(png, info);
    png_byte bit_depth  = png_get_bit_depth(png, info);
    png_byte channels   = png_get_channels(png, info);

    // Read any color_type into 8bit depth, RGBA format.
    // See http://www.libpng.org/pub/png/libpng-manual.txt

    if(bit_depth == 16)
        png_set_strip_16(png);

    if(color_type == PNG_COLOR_TYPE_PALETTE)
        png_set_palette_to_rgb(png);

    // PNG_COLOR_TYPE_GRAY_ALPHA is always 8 or 16bit depth.
    if(color_type == PNG_COLOR_TYPE_GRAY && bit_depth < 8)
        png_set_expand_gray_1_2_4_to_8(png);

    if(png_get_valid(png, info, PNG_INFO_tRNS))
        png_set_tRNS_to_alpha(png);

    // These color_type don't have an alpha channel then fill it with 0xff.
    if(color_type == PNG_COLOR_TYPE_RGB ||
       color_type == PNG_COLOR_TYPE_GRAY ||
       color_type == PNG_COLOR_TYPE_PALETTE) {
        png_set_filler(png, 0xFF, PNG_FILLER_AFTER);
        channels++;
    }

    if(color_type == PNG_COLOR_TYPE_GRAY ||
       color_type == PNG_COLOR_TYPE_GRAY_ALPHA)
        png_set_gray_to_rgb(png);

    png_read_update_info(png, info);

    Image *image = (Image *)malloc(sizeof(Image));
    image->width      = png_get_image_width(png, info);
    image->height     = png_get_image_height(png, info);
    image->channels = channels;

    image->rows = (png_bytep*)malloc(sizeof(png_bytep) * image->height);
    for(int y = 0; y < image->height; y++) {
        image->rows[y] = (png_byte*)malloc(png_get_rowbytes(png, info));
    }

    png_read_image(png, image->rows);

    fclose(fp);

    png_destroy_read_struct(&png, &info, NULL);

    return image;
}

void write_png_file(Image *image, char *filename) {
    int y;

    FILE *fp = fopen(filename, "wb");
    if(!fp) abort();

    png_structp png = png_create_write_struct(PNG_LIBPNG_VER_STRING, NULL, NULL, NULL);
    if (!png) abort();

    png_infop info = png_create_info_struct(png);
    if (!info) abort();

    if (setjmp(png_jmpbuf(png))) abort();

    png_init_io(png, fp);

    // Output is 8bit depth, RGBA format.
    png_set_IHDR(
            png,
            info,
            image->width, image->height,
            8,
            PNG_COLOR_TYPE_RGBA,
            PNG_INTERLACE_NONE,
            PNG_COMPRESSION_TYPE_DEFAULT,
            PNG_FILTER_TYPE_DEFAULT
    );
    png_write_info(png, info);

    // To remove the alpha channel for PNG_COLOR_TYPE_RGB format,
    // Use png_set_filler().
    //png_set_filler(png, 0, PNG_FILLER_AFTER);

    if (!image->rows) abort();

    png_write_image(png, image->rows);
    png_write_end(png, NULL);

    fclose(fp);

    png_destroy_write_struct(&png, &info);
}
