# custom command to run gdb on entire program and save data to json file
import gdb # type: ignore
import json
import os
import re

# custom gdb command
class RunAll(gdb.Command):
    def __init__(self):
        # call super constructor, register command name in gdb
        super(RunAll, self).__init__("runall", gdb.COMMAND_USER)
        # empty dict to hold data at each line
        self.trace_data = {}
    
    def get_program_name(self):
        # Get the full path of the running program
        exec_file = gdb.current_progspace().filename
        if exec_file:
            # return only a.out
            return os.path.basename(exec_file)
        return "trace"  # default

    def get_next_filename(self, base_name):
        # store just the program name
        base = os.path.splitext(base_name)[0]
        # regex for matching
        pattern = re.compile(rf"{re.escape(base)}_(\d+)\.json")

        # list of existing files in current directory
        existing = [f for f in os.listdir(".") if pattern.fullmatch(f)]
        # extract numbers from those files
        numbers = [int(pattern.fullmatch(f).group(1)) for f in existing]

        # next available number for naming the file
        next_num = max(numbers, default=0) + 1
        # final file name
        return f"{base}_{next_num}.json"

    # run gdb on the program and save data
    def invoke(self, args, from_tty):
        # start running gdb at the beggining of main
        gdb.execute("start")
        # get user's working directory
        user_dir = os.getcwd()
        # infinite loop to step through every line of code
        while True:
            # for each line
            try:
                # get current stack frame
                stack = gdb.selected_frame()
                # get source line mapping
                sal = gdb.find_pc_line(stack.pc())
                # filter out lines that are not in user's working directory (libraries, system calls)
                if not sal.symtab or not os.path.abspath(sal.symtab.filename).startswith(user_dir):
                    gdb.execute("step")
                    continue
                # get current scope
                scope = stack.block()
                # create dictionary {variable name : value}
                vars = {}
                # loop through code and find variables
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
                        line = sal.line
                        # add to trace data dictionary, {line num (int): updated vars dictionary}
                        self.trace_data[line] = vars
                # next instruction
                gdb.execute("step")

            except (gdb.error, RuntimeError):
                break
                # end of program
        
        base = self.get_program_name()
        output_file = self.get_next_filename(base)

        # Save the JSON file
        with open(output_file, "w") as f:
            json.dump(self.trace_data, f, indent=2)
RunAll()