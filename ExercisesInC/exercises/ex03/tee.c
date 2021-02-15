#include <stdio.h>
#include <string.h>

/*
 * Continually scans the standard input for new lines and writes them to the
 * file at the provided pointer. Inputs are also written to standard output.
 * 
 * @param output: a FILE* to which the stdin is written
 */
void writeToStreams(FILE* output) {
	// NOTE: I thought a lot about what to actually make the size restriction on the string. I
	// wanted it to be long enough so someone could type a long sentence or whatever, but not
	// too long to consume a ton of memory and potentially cause problems. After some research
	// I stumbled on this constant which is allegedly optimized based on the actual system
	// architecture to make I/O operations more efficient. On my machine its 8192.
	char line[BUFSIZ];

	// NOTES: I was being silly for a very long time and terminating the program with Ctrl+C
	// rather than Ctrl+D. As a result, I could't figure out why this line wasn't actually
	// writing to the file. The `tee` source uses signal interrupts to ensure that the file
	// is written to no matter the exit condition or signal (ie. the output is flushed no matter
	// the terminating SIG.
	//
	// Next time, I am going to look into using the `getline` function. It seems to have some cool
	// features like dynamically-allocated line lengths, but is not implemented on all C distributions
	// and can potentially cause some memory allocation problems if used incorrectly.
	while(fgets(line, BUFSIZ, stdin) != NULL) {
		fprintf(output, line);
		printf("%s", line);
	}
}

int main(int argc, char* argv[]) {
	// NOTE: the official source uses a switch/case statement as well as a ton of more
	// complicated argument type-checking and analysis to ensure that a command is valid
	//
	// verify that the command usage is correct by checking the number args and their values
	if(argc != 3 || (strcmp(argv[1], "-a") != 0 && strcmp(argv[1], "--append") != 0)) {
		fprintf(stderr, "Usage: ./tee --append FILE\n");
		return 1;
	}

	// NOTE: the actual implementation uses raw FILE descriptors rather than pointers, which
	// are lower level and behave closer to the kernel
	//
	// attempt to open the provided file name in "append only" mode
	FILE* out = fopen(argv[2], "a");
	if(out == NULL) {
		// something went wrong opening the file so tell the user
		fprintf(stderr, "Failed to open stream: No such file or directory!\n");
		return 1;
	}

	// scan for user input and append it
	writeToStreams(out);
	// ensure we close the file handle
	fclose(out);
	return 0;
}

// SIDENOTE: there are substantially fewer comments in the official source
