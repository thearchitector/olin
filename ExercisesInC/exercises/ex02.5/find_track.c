/* Example code for Exercises in C.

Modified version of an example from Chapter 2.5 of Head First C.

*/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <regex.h>

#define NUM_TRACKS 5

char tracks[][80] = {
    "So What",
    "Freddie Freeloader",
    "Blue in Green",
    "All Blues",
    "Flamenco Sketches"
};


// Finds all tracks that contain the given string.
//
// Prints track number and title.
void find_track(char search_for[])
{
    int i;
    for (i=0; i<NUM_TRACKS; i++) {
        if (strstr(tracks[i], search_for)) {
            printf("Track %i: '%s'\n", i, tracks[i]);
        }
    }
}

// Finds all tracks that match the given pattern.
//
// Prints track number and title.
void find_track_regex(char pattern[])
{
    // Compile the given pattern into a valid regular expression
    regex_t reg;
    int error = regcomp(&reg, pattern, REG_EXTENDED);
    
    // if an error occured
    if(error != 0) {
	char msg[100];

	// translate the error code into a human-readable string, print it
	// to the console via stderr, and exit the program
	regerror(error, &reg, msg, sizeof(msg));
	fprintf(stderr, "An error occured: %s\n\n", msg);
	exit(1);
    }
    
    int r;
    int i;

    // loop through all the tracks
    for(i = 0; i < NUM_TRACKS; ++i) {
	// try and match the regex to the track name
    	r = regexec(&reg, tracks[i], 0, NULL, 0);

	// if a match was found, print it
	if(r == 0) {
	    printf("Track %i: '%s'\n", i, tracks[i]);
	}
    }

    // free the memory allocated for the compiled regex
    regfree(&reg);
}

// Truncates the string at the first newline, if there is one.
void rstrip(char s[])
{
    char *ptr = strchr(s, '\n');
    if (ptr) {
        *ptr = '\0';
    }
}

int main (int argc, char *argv[])
{
    char search_for[80];

    /* take input from the user and search */
    printf("Search for: ");
    fgets(search_for, 80, stdin);
    rstrip(search_for);

    //find_track(search_for);
    find_track_regex(search_for);

    return 0;
}
