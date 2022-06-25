from imutils.perspective import four_point_transform
from imutils import contours
import numpy as np
import argparse
import imutils
import cv2

# ap = argparse.ArgumentParser()
# ap.add_argument("-i", "--image", required=True, help="path to the input image")
# args = vars(ap.parse_args())

ANSWER_KEY = {0:2, 1:4, 2:0, 3:3, 4:1}

image = cv2.imread('images/omr_test_01.png')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray, (5,5), 0)
edges = cv2.Canny(blur, 75, 200)

countours = cv2.findContours(edges.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
countours = imutils.grab_contours(countours)

page_outline = None

if len(countours) > 0:
    countours = sorted(countours, key= cv2.contourArea, reverse=True)
    for i in countours:
        perimeter = cv2.arcLength(i, True)
        approx = cv2.approxPolyDP(i, 0.02 * perimeter, True)

        if len(approx) == 4:
            page_outline = approx
            break
sheet = four_point_transform(image, page_outline.reshape(4, 2))
wrapped = four_point_transform(gray, page_outline.reshape(4, 2))
otsu_thresh = cv2.threshold(wrapped, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]


cv2.imshow('Example - Show image in window', otsu_thresh)
cv2.waitKey(0)  # waits until a key is pressed
cv2.destroyAllWindows()