mmulrand: matmath.o main.c
	/opt/cuda/bin/nvcc main.c matmath.o -o mmulrand

matmath.o: matmath.cu matmath.h codes.h
	/opt/cuda/bin/nvcc -c matmath.cu -o matmath.o

img.o: img.cpp img.h
	gcc -c img.cpp -lpng

img_test: img_test.cpp img.o
	gcc -o img_test img_test.cpp img.o -lpng

linalg.o: linalg.cpp linalg.h img.o
	gcc -c linalg.cpp -lpng

convolve_test: convolve_test.cpp linalg.o
	gcc -o convolve_test convolve_test.cpp linalg.o img.o -lpng

clean:
	rm *.o
	rm -f img_test
