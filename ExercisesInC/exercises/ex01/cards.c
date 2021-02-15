/*
 * A small application for keeping track of and counting cards input by the user.
 *
 * @author: Elias Gabriel
 * @revision: v1.0.0
 */
#include <stdio.h>
#include <stdlib.h>

/**
 * Prompts the user for a specific card name and updates the contents of the
 * given string buffer.
 *
 * @param prompt: the message to display to the user
 * @param cardName: the string to store the user's response
 */
void getCardName(char* prompt, char* cardName) {
	puts(prompt);
	scanf("%2s", cardName);
}

/**
 * Converts a given card name to a specific point value, or returns -1 to indicate a termination request.
 *
 * @param cardName: the card to convert to a point value
 * @return int: the point value of the card
 */
int getCardValue(char *cardName) {
	int val = 0;
	
	switch(cardName[0]) {
		case 'K':
		case 'Q':
		case 'J':
			val = 10;
			break;
		case 'A':
			val = 11;
			break;
		case 'X':
			return -1;
		default:
			val = atoi(cardName);
			
			if((val < 1) || (val > 10)) {
				puts("I don't understand that value!");
				return -1;
			}
	}

	return val;
}

/**
 * The main method responsible for continually asking the user for a card, converting it to
 * a numerical value, and keeping track of the card count.
 */
int main() {
	char cardName[3];
	int count = 0;
	int val;

	do {
		getCardName("Enter the card number: ", cardName);
		val = getCardValue(cardName);

		if((val > 2) && (val < 7)) {
			count++;
		}
		else if (val == 10) {
			count--;
		}

		printf("Current count: %i\n", count);
	}
	while(cardName[0] != 'X');
	
	return 0;
}
