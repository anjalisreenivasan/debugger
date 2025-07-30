/* 1. variable declaration
    2. undefined print behavior
    3. c library call
    4. return
*/

#include <stdio.h>
#include <stdlib.h>

int main() {
    int a;
    int b;
    printf("%d\n", a);
    a = 1;
    b = 2;
    return 0;
}