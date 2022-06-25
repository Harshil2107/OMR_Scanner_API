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

contours = cv2.findContours(edges.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
contours = imutils.grab_contours(contours)

page_outline = None

if len(contours) > 0:
    contours = sorted(contours, key= cv2.contourArea, reverse=True)
    for i in contours:
        perimeter = cv2.arcLength(i, True)
        approx = cv2.approxPolyDP(i, 0.02 * perimeter, True)

        if len(approx) == 4:
            page_outline = approx
            break
sheet = four_point_transform(image, page_outline.reshape(4, 2))
wrapped = four_point_transform(gray, page_outline.reshape(4, 2))
otsu_thresh = cv2.threshold(wrapped, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

contours = cv2.findContours(otsu_thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

contours = imutils.grab_contours(contours)
question_bubble_contours = []

for i in contours:
    (x,y, w, h) = cv2.boundingRect(i)
    ar = w/float(h)

    if w >- 20 and h>= 20 and ar>= 0.9 and ar <= 1.1:
        question_bubble_contours.append(i)
        cv2.drawContours(sheet, [i], -1, (255,255,0), 2)

cv2.imshow('Example - Show image in window', sheet)
cv2.waitKey(0)  # waits until a key is pressed
cv2.destroyAllWindows()