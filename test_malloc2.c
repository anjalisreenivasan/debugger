#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main() {
    char temp[100];  // temporary buffer to read user input
    printf("Enter a word: ");
    scanf("%s", temp);

    // Allocate memory for the string (including null terminator)
    char *copy = (char *)malloc(strlen(temp) + 1);

    // Check if malloc succeeded
    if (copy == NULL) {
        printf("Memory allocation failed.\n");
        return 1;
    }

    // Copy the string into dynamically allocated memory
    strcpy(copy, temp);

    // Use the string
    printf("You entered: %s\n", copy);

    // Free the memory
    free(copy);
    return 0;
}