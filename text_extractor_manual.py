#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cv2
import sys
import numpy as np

filename = sys.argv[1]

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
    ((550, 433), (706, 452)),   #RESIDENCE PERMIT
]

cv2.namedWindow('rects')

image = cv2.imread(filename)

for box in boxes:
    cv2.rectangle(image, box[0], box[1], (0, 255, 0))

cv2.imshow('rects', image)
cv2.waitKey(0)

cv2.destroyWindow('rects')

for i in range(0, len(boxes)):
    box = boxes[i]

    text = image[box[0][1]:box[1][1], box[0][0]:box[1][0]]

    cv2.imwrite('cutouts/' + str(i) + '.jpg', text)