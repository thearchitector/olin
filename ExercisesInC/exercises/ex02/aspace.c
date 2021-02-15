/* Example code for Think OS.

Copyright 2014 Allen Downey
License: GNU GPLv3

*/

#include <stdio.h>
#include <stdlib.h>

int var1;

int five() {
    int var3 = 42;
    printf ("Address of var3 is %p\n", &var3);
}

int main ()
{
    int var2 = 5;
    void *p = malloc(128);
    void *q = malloc(128);
    char *s = "Hello, World";
    void *rp1 = malloc(27);
    void *rp2 = malloc(27);

    five();

    printf ("Address of main is %p\n", main);
    printf ("Address of var1 is %p\n", &var1);
    printf ("Address of var2 is %p\n", &var2);
    printf ("p points to %p\n", p);
    printf ("q points to %p\n", q);
    printf ("s points to %p\n", s);
    printf ("rp1 %p\n", rp1);
    printf ("rp2 %p\n", rp2);

    return 0;
}
