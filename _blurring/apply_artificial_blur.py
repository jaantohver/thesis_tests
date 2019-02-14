import cv2
import numpy as np
from subprocess import call

call(["rm", "-rf", "res_downscaled"])
call(["mkdir", "res_downscaled"])

img = cv2.imread('doc_reg/input_downscaled.jpg')
# cv2.imshow('Original', img)

count = 1

for kernel_size in range(3, 23, 2):
    # generating the kernel
    kernel_motion_blur = np.zeros((kernel_size, kernel_size))
    kernel_motion_blur[int((kernel_size - 1) / 2), :] = np.ones(kernel_size)
    kernel_motion_blur = kernel_motion_blur / kernel_size

    print("---")
    print(count)
    print(kernel_motion_blur)

    # applying the kernel to the input image
    output = cv2.filter2D(img, -1, kernel_motion_blur)

    # cv2.imshow('Motion Blur ' + str(kernel_size), output)
    cv2.imwrite('res_downscaled/' + str(count) + '.jpg', output)
    count += 1

# cv2.waitKey(0)
