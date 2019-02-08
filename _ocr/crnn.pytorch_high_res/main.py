import sys
from subprocess import call

if len(sys.argv) < 2:
    print("No input folder specified.")
    exit()

if len(sys.argv) < 3:
    print("No output folder specified.")
    exit()

input_folder = sys.argv[1]
output_folder = sys.argv[2]

call(["python", "demo.py", input_folder, output_folder])
