/**
 * Allows the user to enter integers, one per line, until the user hits Control-D.
 * Sums the array and prints the results.
 *
 * @author: Elias Gabriel
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>


// Find the sum of the given array and print the result
int sum(int nums[], int count) {
	int sum = 0;
	int i;

	for(i = 0; i <= count; ++i) sum += nums[i];

	printf("The sum of the inputs is: %d\n", sum);
	return 0;
}

int main() {
	char input[12];
	int nums[50];
	int count = -1;
	int tmp;

	printf("Enter numbers to sum, one on each line...\n");

	while(fgets(input, 11, stdin) != NULL) {
		tmp = atoi(input);
		
		if(tmp == 0 && strlen(input) > 2) {
			printf("That's not a valid number!\n");
			return 1;
		}
		else {
			nums[++count] = tmp;
		}
	}

	sum(nums, count);
}

