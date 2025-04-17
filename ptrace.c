#include <stdio.h>
#include <stdlib.h>
#include <sys/ptrace.h>
#include <sys/wait.h>
#include <sys/types.h>
#include <unistd.h>

int main (void) {
    pid_t child = fork();

    if (child == -1){
        //error
    } else if (child == 0){
        ptrace(PT_TRACE_ME, 0, NULL, 0);
        execl("sample.c", "sample", NULL);
    } else {
        int status;
        waitpid(child, &status, 0);
    }

}