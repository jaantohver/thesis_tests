import cv2
import sys

filename = sys.argv[1]

cv2.namedWindow("result")

def detectLetters(img):
    #img = cv2.resize(img, None, fx=0.25, fy=0.25, interpolation=cv2.INTER_CUBIC)

    cv2.imshow('result', img)
    cv2.waitKey(0)

    boundRect = []
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    cv2.imshow('result', img_gray)
    cv2.waitKey(0)

    img_sobel = cv2.Sobel(img_gray, cv2.CV_8U, dx=1, dy=0, ksize=3, scale=1, delta=0, borderType=cv2.BORDER_DEFAULT)

    cv2.imshow('result', img_sobel)
    cv2.waitKey(0)

    _, img_threshold = cv2.threshold(img_sobel, 0, 255, cv2.THRESH_OTSU+cv2.THRESH_BINARY)

    cv2.imshow('result', img_threshold)
    cv2.waitKey(0)

    element = cv2.getStructuringElement(cv2.MORPH_RECT, (17, 3))
    img_threshold = cv2.morphologyEx(img_threshold, cv2.MORPH_CLOSE, element)

    cv2.imshow('result', img_threshold)
    cv2.waitKey(0)

    _, contours, _ = cv2.findContours(img_threshold, 0, 1)
    
    for contour in contours:
        if len(contour) > 100:
            contour_poly = cv2.approxPolyDP(contour, 3, True)
            x, y, w, h = cv2.boundingRect(contour_poly)
            if w > h:
                boundRect.append((x, y, w, h))

    # img_threshold = cv2.cvtColor(img_threshold, cv2.COLOR_GRAY2BGR)
    # cv2.drawContours(img_threshold, contours, -1, (0, 255, 0), 3)

    # cv2.namedWindow("test")
    # cv2.imshow("test", img_threshold)
    # cv2.waitKey(0)
    # cv2.destroyWindow("test")

    return boundRect;

#Read
# cv::Mat img1=cv::imread("side_1.jpg");
img1 = cv2.imread(filename)

# cv::Mat img2=cv::imread("side_2.jpg");
# img2 = cv2.imread("id_2.jpg")

#Detect
# std::vector<cv::Rect> letterBBoxes1=detectLetters(img1);
letterBBoxes1 = detectLetters(img1)

# std::vector<cv::Rect> letterBBoxes2=detectLetters(img2);
# letterBBoxes2 = detectLetters(img2)

#Display
# for(int i=0; i< letterBBoxes1.size(); i++)
for i in range(len(letterBBoxes1)):
    # cv::rectangle(img1,letterBBoxes1[i],cv::Scalar(0,255,0),3,8,0);
    pt1 = (letterBBoxes1[i][0], letterBBoxes1[i][1])
    pt2 = (letterBBoxes1[i][0] + letterBBoxes1[i][2], letterBBoxes1[i][1] + letterBBoxes1[i][3])
    cv2.rectangle(img1, pt1, pt2, (0, 255, 0), 3, 8, 0)
# cv::imwrite( "imgOut1.jpg", img1);
# cv2.imwrite("imgOut1.jpg", img1)

cv2.imshow("result", img1)
cv2.waitKey(0)
cv2.destroyWindow("result")

# for(int i=0; i< letterBBoxes2.size(); i++)
# for i in range(len(letterBBoxes2)):
    # cv::rectangle(img2,letterBBoxes2[i],cv::Scalar(0,255,0),3,8,0);
    # pt1 = (letterBBoxes2[i][0], letterBBoxes2[i][1])
    # pt2 = (letterBBoxes2[i][0] + letterBBoxes2[i][2], letterBBoxes2[i][1] + letterBBoxes2[i][3])
    # cv2.rectangle(img2, pt1, pt2, (0, 255, 0), 3, 8, 0)
# cv::imwrite( "imgOut2.jpg", img2);
# cv2.imwrite("imgOut2.jpg", img2)



print("Done!")