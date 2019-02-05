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
    ((365, 95), (487, 117)),  # ELAMISLUBA
    # ((572, 98), (698, 119)),  # BB0021535
    ((328, 137), (352, 151)),  # NIMI
    # ((329, 154), (455, 171)),  # ANBARJAFARI
    # ((329, 171), (455, 189)),  # GHOLAMREZA
    ((329, 194), (384, 205)),  # KEHTIV KUNI
    # ((329, 207), (420, 225)),  # 05.08.2021
    ((329, 227), (468, 240)),  # VÄLJAANDMISE KOHT JA KUUPÄEV
    # ((329, 242), (467, 260)),  # PPA, 05.08.2016
    ((329, 262), (365, 273)),  # LOA LIIK
    # ((329, 275), (543, 294)),  # ELAMISLUBA TÖÖTAMISEKS
    ((329, 313), (379, 323)),  # MÄRKUSED
    # ((329, 325), (484, 343)),  # RESIDENCE PERMIT
    # ((329, 343), (480, 359)),  # FOR EMPLOYMENT
    # ((329, 359), (510, 375)),  # KUNI/UNTIL 31.08.2021
    # ((592, 342), (702, 367)),  # 400688
    ((550, 433), (706, 452)),  # RESIDENCE PERMIT
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
    #     cv2.rectangle(image, box[0], box[1], (0, 255, 0))

    for i in range(0, len(boxes)):
        box = boxes[i]

        text = image[box[0][1]:box[1][1], box[0][0]:box[1][0]]

        cv2.imwrite('res/' + output_folder + '/' + file.split('.')[0] + '/' + sys.argv[i + 3] + '.jpg', text)
