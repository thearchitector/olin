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

typedef struct image {
    unsigned int channels;
    unsigned int width;
    unsigned int height;
    unsigned char **rows;

    /**
     * Attempts to set the value of a pixel.
     * @param row the row (or y-coordinate) of the pixel
     * @param col the column (or x-coordinate) of the pixel
     * @param val the new value to set the pixel to (between 0 and 255, inclusive).
     *   If the image consists of more than one channel, then val should be an array
     *   of unsigned chars with the same length as the number of channels in the image.
     * @return true if row and col are within the bounds of the image, false otherwise
     */
    bool set_pixel(unsigned int row, unsigned int col, unsigned char *val);

    /**
     * Attempts to get the value of a pixel.
     * @param row the row (or y-coordinate) of the pixel
     * @param col the column (or x-coordinate) of the pixel
     * @param res where to put the result (should be of size char times the number
     *   of channels in the image)
     * @return true if row and col are within the bounds of the image, false otherwise
     */
    bool get_pixel(int row, int col, unsigned char *res);

    /**
     * Prints out a grid of pixel values for each channel.
     */
    void print_channels();

    /**
     * Copies over the data from the specified channel of the source image.
     * @param src the image to copy data from
     * @param srcChannel the channel to copy data from in the source image
     * @param destChannel the channel to copy the data to
     * @return false if the dimensions in the two images don't match
     *  or if the channel indexes are out of range of their respective images,
     *  true otherwise
     */
    bool copy_channel(image *src, int srcChannel, int destChannel);
} Image;

/**
 * Creates a new blank image with all pixels and all channels set to 0.
 * @param width the width of the image
 * @param height the height of the image
 * @param channels the number of channels for each pixel
 * @return a new Image
 */
Image *create_blank_image(unsigned int width, unsigned int height, unsigned int channels);
Image *read_png_file(char *filename);
void write_png_file(Image *image, char *filename);
