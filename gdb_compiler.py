# compiles and runs custom runall command
import os
import subprocess
import sys
import tempfile

# 1 command line arg, source file
if len(sys.argv) != 2:
    sys.exit(1)

source_file = sys.argv[1]

# isolate file name
executable = os.path.splitext(source_file)[0]

# prepare command for compilation
compile_command = ["gcc", "-g", source_file, "-o", executable]

# compile the program
try:
    subprocess.run(compile_command, check=True)
except subprocess.CalledProcessError:
    sys.exit(1) # tell the user hello??

# create temp gdb script
script = tempfile.NamedTemporaryFile(delete=False, mode = 'w', suffix='.gdb')

# get and write absolute path to run from any directory
abs_path = os.path.join(os.path.dirname(__file__), "gdb_tracer.py")
script.write(f"source {abs_path}\n")
script.write("python print('TRACER LOADED YEAH YEAH YEAH')\n")

# write gdb instructions to script
script.write("runall\n")
script.write("quit\n")
script.close()

# run script
subprocess.run(["gdb", "-q", "-x", script.name, executable])

# delete script
os.unlink(script.name)