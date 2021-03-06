# The MIT License (MIT)

# Copyright (c) 2017 Dhanushka Dangampola

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

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

input_folder = sys.argv[1]
output_folder = sys.argv[2]

call(["rm", "-rf", "res"])
call(["mkdir", "res"])

files = os.listdir(input_folder)
files.sort()

for file in files:
    if ".jpg" not in file:
        continue

    call(["mkdir", "res/" + output_folder + "/" + file.split('.')[0]])

    large = cv2.imread(input_folder + "/" + file)

    # cv2.imshow('rects', large)
    # cv2.waitKey(0)

    rgb = cv2.pyrDown(large)

    # cv2.imshow('rects', rgb)
    # cv2.waitKey(0)

    small = cv2.cvtColor(rgb, cv2.COLOR_BGR2GRAY)

    # cv2.imshow('rects', small)
    # cv2.waitKey(0)

    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    grad = cv2.morphologyEx(small, cv2.MORPH_GRADIENT, kernel)

    # cv2.imshow('rects', grad)
    # cv2.waitKey(0)

    _, bw = cv2.threshold(grad, 0.0, 255.0, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

    # cv2.imshow('rects', bw)
    # cv2.waitKey(0)

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (9, 1))
    connected = cv2.morphologyEx(bw, cv2.MORPH_CLOSE, kernel)

    # cv2.imshow('rects', connected)
    # cv2.waitKey(0)

    # using RETR_EXTERNAL instead of RETR_CCOMP
    contours, hierarchy = cv2.findContours(connected.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    mask = np.zeros(bw.shape, dtype=np.uint8)

    # cv2.drawContours(rgb, contours, -1, (0, 255, 0))

    # cv2.imshow('rects', rgb)
    # cv2.waitKey(0)

    for idx in range(len(contours)):
        x, y, w, h = cv2.boundingRect(contours[idx])
        mask[y:y + h, x:x + w] = 0
        cv2.drawContours(mask, contours, idx, (255, 255, 255), -1)
        r = float(cv2.countNonZero(mask[y:y + h, x:x + w])) / (w * h)

        if r > 0.45 and w > 8 and h > 8:
            cv2.rectangle(rgb, (x, y), (x + w - 1, y + h - 1), (0, 255, 0), 2)

    cv2.imshow('rects', rgb)
    cv2.waitKey(0)

    cv2.destroyWindow('rects')
