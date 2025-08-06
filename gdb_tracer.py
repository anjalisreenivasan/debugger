# custom command to run gdb on entire program and save data to json file
import gdb # type: ignore
import json
import os
import re
import copy

# custom gdb command
class RunAll(gdb.Command):
    def __init__(self):
        # call super constructor, register command name in gdb
        super(RunAll, self).__init__("runall", gdb.COMMAND_USER)
        # empty dict to hold data at each line, {line : vars dict}
        self.trace_data = []
        self.vars = {}
        # user workspace directory for vs code extension or empty 
        self.workspace_root = os.environ.get("VSCODE_WORKSPACE_ROOT", "").strip()
        if self.workspace_root:
            # vs code
            self.workspace_root = os.path.abspath(self.workspace_root)
        else:
            # docker
            self.workspace_root = os.getcwd()
    
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
        gdb.execute("step")
        # infinite loop to step through every line of code
        while True:
            try:
                # get current stack frame
                stack = gdb.selected_frame()
                # get source line mapping
                sal = gdb.find_pc_line(stack.pc())

                # filters out frames that map to non source files (assembly..)
                if not sal.symtab:
                    gdb.execute("step")
                    continue

                src_path = os.path.abspath(sal.symtab.filename)

                if self.workspace_root and src_path.startswith(self.workspace_root):
                     pass #vs code
                elif sal.symtab and ".c" in sal.symtab.filename:
                     pass  # docker
                else:
                     gdb.execute("step")
                     continue

                # get current scope
                scope = stack.block()
                # temporary vars dict for current state
                snapshot_vars = {}
                # loop through code and find variables
                for symbol in scope:
                    if symbol.is_variable:
                        try:
                            # read value of variable in current frame, uses name of symbol to get value
                            value = stack.read_var(symbol.name)
                            if symbol.name not in snapshot_vars:
                                snapshot_vars[symbol.name] = [str(value)]
                            else:
                                snapshot_vars[symbol.name].append(str(value))
                        except:
                            snapshot_vars[symbol.name] = ["undefined"]
                line = sal.line
                self.vars = snapshot_vars
                self.trace_data.append({line: copy.deepcopy(self.vars)})
                
                # quit at the return statement in main
                if stack.name() == "main":
                    try:
                        with open(src_path, "r") as file:
                            lines = file.readlines()
                            curr_line = lines[sal.line - 1].strip()
                        if curr_line.startswith("return"):
                            break
                    except FileNotFoundError:
                        pass

                # next instruction
                gdb.execute("step")

            except (gdb.error, RuntimeError):
                break
                # end of program
        base = self.get_program_name()
        output_file = self.get_next_filename(base)

        # Save the JSON file
        with open(output_file, "w") as f:
            for entry in self.trace_data:
                f.write(json.dumps(entry) + "\n")
RunAll()