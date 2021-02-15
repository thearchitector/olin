trout: util.o main.o trout.o
	gcc -Wall main.o util.o trout.o -o trout

trout.o: trout.h trout.c main.c
	gcc -Wall -c main.c trout.c

util.o: util.h util.c
	gcc -Wall -c util.c
