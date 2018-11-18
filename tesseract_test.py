import os
import cv2
import sys
import subprocess
import xml.etree.ElementTree as ET

filename = sys.argv[1]

img = cv2.imread(filename)

subprocess.check_output(['tesseract', filename, 'out', '-l', 'est+eng', '--psm', '11'])


tree = ET.parse('out.hocr')
root = tree.getroot()

for child in root[1][0]:
    _, x, y, x2, y2 = child.attrib['title'].split(' ')

    cv2.rectangle(img, (int(x), int(y)), (int(x2), int(y2)), (0, 255, 0), 2)

cv2.namedWindow('rects')



cv2.imshow('rects', img)
cv2.waitKey(0)