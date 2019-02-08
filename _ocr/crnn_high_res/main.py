import sys
from subprocess import call

if len(sys.argv) < 2:
    print("No input folder specified.")
    exit()

input_folder = sys.argv[1]

call(["rm", "-rf", "res"])
call(["mkdir", "res"])

print("tuut")

call(["th", "src/demo.lua"])
