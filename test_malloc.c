#include <stdio.h>
#include <stdlib.h>

int main() {
    int *arr;
    int size = 5;

    // Allocate memory for 5 integers
    arr = (int *)malloc(size * sizeof(int));

    // Check if malloc succeeded
    if (arr == NULL) {
        printf("Memory allocation failed.\n");
        return 1;
    }

    // Assign values and print them
    for (int i = 0; i < size; i++) {
        arr[i] = i * 2;
        printf("arr[%d] = %d\n", i, arr[i]);
    }

    // Free the allocated memory
    free(arr);

    return 0;
}
