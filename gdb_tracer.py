import gdb
import json

# custom gdb command
class RunAll(gdb.Command):
    def __init__(self):
        # register command name in gdb
        super(RunAll, self).__init__("runall", gdb.COMMAND_USER)
        # initialize empty list to hold data at each line
        self.trace_data = []

    # run gdb on the program and save data
    def invoke(self, args, from_tty):
        # start running gdb at the beggining of main
        gdb.execute("start")
        # infinite loop to step through every line of code
        while True:
            # for each line
            try:
                # get current stack frame
                stack = gdb.selected_frame()
                # get current scope
                scope = stack.block()
                # create dictionary {symbol: value}
                vars = {}
                # loop through code and find variables
                # symbol is an object with a set of functions you can use, automatically an object when u iterate scope
                for symbol in scope:
                    if symbol.is_variable:
                        try:
                            # read value of variable in current frame, uses name of symbol to get value
                            value = stack.read_var(symbol.name)
                            # save symbol & string version of value to dictionary (string for json later)
                            vars[symbol.name] = str(value)
                        except:
                            vars[symbol.name] = "undefined"
                        # get the curr line number where the symbol is using program counter
                        line = gdb.find_pc_line(stack.pc).line
                        # add to trace data dictionary, {line num (int): updated vars dictionary}
                        self.trace_data[line] = vars
                # next line
                gdb.execute("next")

            except:
                # end of program




                        





