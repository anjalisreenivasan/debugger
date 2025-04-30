import os
import subprocess
import sys
import tempfile

if len(sys.argv) != 2:
    sys.exit(1)

source_file = sys.argv[1]

executable = os.path.splitext(source_file)[0]

compile_command = ["gcc", "-g", source_file, "-o", executable]

try:
    subprocess.run(compile_command, check=True)
except subprocess.CalledProcessError:
    sys.exit(1)

script = tempfile.NamedTemporaryFile(delete=False, mode = 'w', suffix='.gdb')

script.write("source gdb_tracer.py\n")
script.write("runall\n")
script.write("quit\n")
script.close()

subprocess.run(["gdb", "-q", "-x", script.name, executable])

os.unlink(script.name)