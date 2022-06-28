from imutils.perspective import four_point_transform
from imutils import contours
import numpy as np
import imutils
import cv2

ANSWER_KEY = None
"B E A C B"
def set_anskey(key):
    global ANSWER_KEY
    ANSWER_KEY = key
    print(ANSWER_KEY)
def grade_omr(image):
    # image = cv2.imread(url)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blur, 75, 200)

    img_contours = cv2.findContours(edges.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    img_contours = imutils.grab_contours(img_contours)

    page_outline = None

    if len(img_contours) > 0:
        img_contours = sorted(img_contours, key=cv2.contourArea, reverse=True)
        for i in img_contours:
            perimeter = cv2.arcLength(i, True)
            approx = cv2.approxPolyDP(i, 0.02 * perimeter, True)

            if len(approx) == 4:
                page_outline = approx
                break
    wrapped = four_point_transform(gray, page_outline.reshape(4, 2))
    otsu_thresh = cv2.threshold(wrapped, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

    img_contours = cv2.findContours(otsu_thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    img_contours = imutils.grab_contours(img_contours)
    question_bubble_contours = []

    for i in img_contours:
        (x, y, w, h) = cv2.boundingRect(i)
        ar = w / float(h)

        if w > - 20 and h >= 20 and ar >= 0.9 and ar <= 1.1:
            question_bubble_contours.append(i)

    question_bubble_contours = contours.sort_contours(question_bubble_contours, method="top-to-bottom")[0]
    res = 0

    for (q, i) in enumerate(np.arange(0, len(question_bubble_contours), 5)):
        img_contours = contours.sort_contours(question_bubble_contours[i:i + 5])[0]
        marked = None

        for (j, c) in enumerate(img_contours):
            mask = np.zeros(otsu_thresh.shape, dtype="uint8")
            cv2.drawContours(mask, [c], -1, 255, -1)

            mask = cv2.bitwise_and(otsu_thresh, otsu_thresh, mask=mask)
            total = cv2.countNonZero(mask)

            if marked is None or total > marked[0]:
                marked = (total, j)
        k = ANSWER_KEY[q]
        if k == marked[1]:
            res += 1
    return res







