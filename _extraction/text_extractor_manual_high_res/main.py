#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import cv2
import sys
import numpy as np
from subprocess import call

if len(sys.argv) < 2:
    print("No input folder specified.")
    exit()

if len(sys.argv) < 3:
    print("No output folder specified.")
    exit()

if len(sys.argv) < 4:
    print("No ground truth list specified.")
    exit()

input_folder = sys.argv[1]
output_folder = sys.argv[2]

boxes = [
    ((1370, 650), (1620, 700)),   # EESNIMED
    ((1370, 1045), (1520, 1100)),  # SUGU
    ((1370, 1200), (1730, 1255)),  # KODAKONDSUS
    ((1370, 1355), (1620, 1410)),  # SÜNNIAEG
    ((1365, 1520), (1630, 1575)),  # ISIKUKOOD
    ((1365, 1675), (1880, 1730)),  # DOKUMENDI NUMBER
    ((1360, 2000), (1665, 2050)),  # KEHTIV KUNI
]

call(["rm", "-rf", "res"])
call(["mkdir", "res"])
call(["mkdir", "res/" + output_folder])

files = os.listdir(input_folder)
files.sort()

for file in files:
    if ".jpg" not in file:
        continue

    call(["mkdir", "res/" + output_folder + "/" + file.split('.')[0]])

    full_path = input_folder + '/' + file

    image = cv2.imread(full_path)

    # for box in boxes:
    #     cv2.rectangle(image, box[0], box[1], (0, 0, 255))

    # small = cv2.resize(image, (0, 0), fx=0.25, fy=0.25)
    # cv2.imshow('res', image)
    # cv2.waitKey(0)

    for i in range(0, len(boxes)):
        box = boxes[i]

        text = image[box[0][1]:box[1][1], box[0][0]:box[1][0]]

        cv2.imwrite('res/' + output_folder + '/' + file.split('.')[0] + '/' + sys.argv[i + 3] + '.jpg', text)
