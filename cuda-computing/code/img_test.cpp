#include "img.h"
#include <stdlib.h>
#include <stdio.h>

void invert(unsigned char *px) {
    for (int i = 0; i < 3; ++i) {
        px[i] = (255 - px[i]);
    }
}

void process_png_file(Image *image) {
    unsigned char *px = (unsigned char *)malloc(sizeof(char) * image->channels);
    for(int y = 0; y < image->height; y++) {
        for(int x = 0; x < image->width; x++) {
            if (!image->get_pixel(y, x, px)) return;
            invert(px);
            image->set_pixel(y, x, px);
        }
    }
}

int main(int argc, char *argv[]) {
    if(argc != 3) return 1;

    Image *image = read_png_file(argv[1]);
    print_image_pixels(image);
    write_png_file(image, argv[2]);

    return 0;
}
