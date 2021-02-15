//
// Created by Kyle Combes on 3/20/20 for Software Systems at Olin College.
//

#include "linalg.h"
#include <stdlib.h>
#include <stdio.h>

int main(int argc, char *argv[]) {
    if(argc != 3) {
	    printf("USAGE: convolve_test <path_to_source_img.png> <output_file_name.png>");
	    return 1;
    }

    Image *image = read_png_file(argv[1]);
    float row1[] = {0.0625, 0.125, 0.0625};
    float row2[] = {0.125, 0.25, 0.125};
    float row3[] = {0.0625, 0.125, 0.0625};
    float **blurDef = (float **)malloc(sizeof(float *) * 3);
    blurDef[0] = row1;
    blurDef[1] = row2;
    blurDef[2] = row3;

    Kernel *blur = create_kernel(3, 3, blurDef);
    Image *res = convolve(image, blur);

    write_png_file(res, argv[2]);

    return 0;
}
