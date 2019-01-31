import sys
from subprocess import call

if len(sys.argv) < 2:
    print("No input folder specified.")
    exit()

if len(sys.argv) < 3:
    print("No ground truth list specified.")
    exit()

input_folder = sys.argv[1]
ground_truth = sys.argv[2:]

call(["rm", "-rf", "res"])
call(["mkdir", "res"])

call(["python", "demo.py", input_folder] + ground_truth)
