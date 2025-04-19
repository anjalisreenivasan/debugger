import gdb
import json

class RunAll(gdb.Command):
    def __init__(self):
        # register command name in gdb
        super(RunAll, self).__init__("runall", gdb.COMMAND_USER)
        # initialize empty list to hold trace data at each line
        self.trace_data = []

    # run gdb on the program and save data
    def invoke(self, args, from_tty):
        # start running gdb at the beggining of main
        gdb.execute("start")
        # infinite loop to step through every line of code
        while True:
            try:
                # get current stack frame
                stack = gdb.selected_frame()
                # get current scope
                scope = stack.block()
                # create dictionary {variable: value}
                vars = {}
                # loop through code and find variables
                for symbol in scope:
                    if symbol.is_variable:
                        try:
                            # rea value of variable in current frame
                            value = stack.read_var(symbol.name)
                        except:
                            #idk whatever
                        # curr line number using program counter
                        line = gdb.find_pc_line(stack.pc).line
                        



                        





