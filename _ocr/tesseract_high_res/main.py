#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import cv2
import sys
import subprocess
import numpy as np
import xml.etree.ElementTree as ET
from subprocess import call
from subprocess import check_output

if len(sys.argv) < 2:
    print("No input folder specified.")
    exit()

if len(sys.argv) < 3:
    print("No output folder specified.")
    exit()

call(["rm", "-rf", "res"])
call(["mkdir", "res"])

input_folder = sys.argv[1]
output_folder = sys.argv[2]


def levenshtein(seq1, seq2):
    size_x = len(seq1) + 1
    size_y = len(seq2) + 1
    matrix = np.zeros((size_x, size_y))
    for x in range(size_x):
        matrix[x, 0] = x
    for y in range(size_y):
        matrix[0, y] = y

    for x in range(1, size_x):
        for y in range(1, size_y):
            if seq1[x - 1] == seq2[y - 1]:
                matrix[x, y] = min(
                    matrix[x - 1, y] + 1,
                    matrix[x - 1, y - 1],
                    matrix[x, y - 1] + 1
                )
            else:
                matrix[x, y] = min(
                    matrix[x - 1, y] + 1,
                    matrix[x - 1, y - 1] + 1,
                    matrix[x, y - 1] + 1
                )

    return (matrix[size_x - 1, size_y - 1])

for dirname, dirnames, filenames in os.walk(input_folder):
    if len(filenames) > 0:
        if any('jpg' in s for s in filenames):
            count = 0
            relativeAccuracy = 0
            true_count = 0
            false_count = 0
            file_count = sum(1 for _ in ('jpg' in s for s in filenames))

            res_folder = "res/" + output_folder + '/' + dirname.split('/')[-1]
            res_file = res_folder + "/output.txt"
            call(["mkdir", "-p", res_folder])
            call(["touch", res_file])

            for filename in filenames:
                if ".jpg" not in filename:
                    continue

                true_label = filename.split('.')[0]
                true_label = ''.join(c for c in true_label if c.isalnum()).lower()

                subprocess.check_output(
                    ['tesseract',
                     dirname + "/" + filename,
                     'tmp',
                     '-l',
                     'est',
                     '--psm',
                     '7'])

                t_file = open('tmp.txt', "r")
                res = t_file.readline()
                res = ''.join(c for c in res if c.isalnum()).lower()

                os.remove("tmp.txt")

                count += 1

                if true_label == res:
                    true_count += 1
                else:
                    false_count += 1

                levDis = levenshtein(true_label, res)
                bigger = max(len(true_label), len(res))
                pct = (bigger - levDis) / bigger
                relativeAccuracy += (pct * 100) / file_count

                f = open(res_file, "a")
                f.write(str(true_label) + " - " + res + " - " + str((pct * 100)) + "\n")

            if true_count is 0:
                f.write("Accuracy = 0%\n")
            else:
                f.write("True count = " + " " + str(true_count) + "; false count = " + str(false_count) +
                        "; accuracy = " + str(true_count * 100 / count) + "%\n")

            f.write("Relative accuracy = " + str(relativeAccuracy) + "%\n")

# tree = ET.parse('out.hocr')
# root = tree.getroot()

# for child in root[1][0]:
#     _, x, y, x2, y2 = child.attrib['title'].split(' ')

#     cv2.rectangle(img, (int(x), int(y)), (int(x2), int(y2)), (0, 255, 0), 2)
