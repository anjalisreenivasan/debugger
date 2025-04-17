# Makefile

ptrace: ptrace.o
	gcc -o ptrace ptrace.o
ptrace.o: ptrace.c
	gcc -c ptrace.c

all: clean ptrace

clean:
	@echo "Cleaning"
	@rm -f *.o ptrace a.out
