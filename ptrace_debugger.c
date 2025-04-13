#include <stdio.h>
#include <stdlib.h>
#include <sys/ptrace.h>
#include <sys/wait.h>
#include <sys/types.h>
#include <unistd.h>

void assembly_debugger(pid_t child);

int main() {
    // create child process
    pid_t child = fork();
    
    //child process
    if (child == 0){
        //child being traced
        ptrace(PT_TRACE_ME, 0, NULL, NULL);
    } else { // parent runs debugger
        debugger(child);
    }
}

void assembly_debug(pid_t child){
    //assembly debugger code
}