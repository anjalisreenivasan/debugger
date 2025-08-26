#include <stdio.h>
#include <stdlib.h>

int main() {
    int x = 11;
    int *ptr = &x;
    int y = *ptr;
    *ptr = 12;
    int z = *ptr;
    return 0;
}