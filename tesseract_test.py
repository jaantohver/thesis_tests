#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import cv2
import sys
import subprocess
import numpy as np
import xml.etree.ElementTree as ET

imageFiles = [
    'doc_blur/1.jpg',
    'doc_blur/2.jpg',
    'doc_blur/3.jpg',
    'doc_blur/4.jpg',
    'doc_blur/5.jpg',
    'doc_blur/6.jpg',
    'doc_blur/7.jpg',
    'doc_blur/8.jpg',
    'doc_blur/9.jpg',
    'doc_blur/10.jpg'
]

imageFiles = [
    'srndeblur_out/1.jpg',
    'srndeblur_out/2.jpg',
    'srndeblur_out/3.jpg',
    'srndeblur_out/4.jpg',
    'srndeblur_out/5.jpg',
    'srndeblur_out/6.jpg',
    'srndeblur_out/7.jpg',
    'srndeblur_out/8.jpg',
    'srndeblur_out/9.jpg',
    'srndeblur_out/10.jpg'
]

boxes = [
    ((365, 95), (487, 117)),    #ELAMISLUBA
    ((572, 98), (698, 119)),    #BB0021535
    ((328, 137), (352, 151)),   #NIMI
    ((329, 154), (455, 171)),   #ANBARJAFARI
    ((329, 171), (455, 189)),   #GHOLAMREZA
    ((329, 194), (384, 205)),   #KEHTIV KUNI
    ((329, 207), (420, 225)),   #05.08.2021
    ((329, 227), (468, 240)),   #VÄLJAANDMISE KOHT JA KUUPÄEV
    ((329, 242), (467, 260)),   #PPA, 05.08.2016
    ((329, 262), (365, 273)),   #LOA LIIK
    ((329, 275), (543, 294)),   #ELAMISLUBA TÖÖTAMISEKS
    ((329, 313), (379, 323)),   #MÄRKUSED
    ((329, 325), (484, 343)),   #RESIDENCE PERMIT
    ((329, 343), (480, 359)),   #FOR EMPLOYMENT
    ((329, 359), (510, 375)),   #KUNI/UNTIL 31.08.2021
    ((592, 342), (702, 367)),   #400688
    ((550, 433), (706, 452))    #RESIDENCE PERMIT
]

# cv2.namedWindow('rects')

fileCounter = 1

for imageFile in imageFiles:
    image = cv2.imread(imageFile)

    boxCounter = 1

    for box in boxes:
        text = image[box[0][1]:box[1][1], box[0][0]:box[1][0]]

        #cv2.rectangle(image, box[0], box[1], (0, 255, 0))
        #cv2.imwrite('doc_blur/5_segment.jpg', image)

        cv2.imwrite('cutouts/' + str(fileCounter) + '_' + str(boxCounter) + '.jpg', text)

        #subprocess.check_output(
        #    ['tesseract',
        #    'cutouts/' + str(fileCounter) + '_' + str(boxCounter) + '.jpg',
        #    'tess_results/out' + str(fileCounter) + '_' + str(boxCounter),
        #    '-l',
        #    'est',
        #    '--psm',
        #    '8'])

        boxCounter += 1

    fileCounter += 1

    # tree = ET.parse('out.hocr')
    # root = tree.getroot()

    # for child in root[1][0]:
    #     _, x, y, x2, y2 = child.attrib['title'].split(' ')

    #     cv2.rectangle(img, (int(x), int(y)), (int(x2), int(y2)), (0, 255, 0), 2)

# cv2.waitKey(0)
# cv2.destroyWindow('rects')