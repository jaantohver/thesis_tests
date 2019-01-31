import sys
from subprocess import call

if len(sys.argv) < 2:
    print("No input folder specified.")
    exit()

input_folder = sys.argv[1]

call(["rm", "-rf", "res"])
call(["mkdir", "res"])
call(["python", "run_model.py", "--input_path=" + input_folder, "--output_path=./res"])
