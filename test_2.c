#include <stdio.h>
#include <stdlib.h>

int main() {
    int counter = 0; // garbage
    int i; // 0
    for (i = 0; i < 3; i++){ // 0
        counter++; // 0, 1, 2
    } // 3
    return counter; // 3
} // 3