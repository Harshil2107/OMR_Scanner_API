from imutils.perspective import four_point_transform
from imutils import contours
import numpy as np
import argparse
import imutils
import cv2

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="path to the input image")
args = vars(ap.parse_args())

ANSWER_KEY = {0:2, 1:4, 2:0, 3:3, 4:1}

image = cv2.imread('images/omr_test_01.png')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray, (5,5), 0)
edges = cv2.Canny(blur, 75, 200)
cv2.imshow('Example - Show image in window', edges)

cv2.waitKey(0)  # waits until a key is pressed
cv2.destroyAllWindows()