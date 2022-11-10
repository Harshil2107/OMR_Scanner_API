import cv2
import imutils
import numpy as np
from imutils import contours
from imutils.perspective import four_point_transform

ANSWER_KEY = None
OPTIONS = None


def set_anskey_num_options(key, options):
    global ANSWER_KEY, OPTIONS
    ANSWER_KEY = key
    OPTIONS = options

def getkey():
    return ANSWER_KEY

def getoptions():
    return OPTIONS

def grade_omr(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blur, 75, 200)
    # getting all the contours from the image on which we applied edge detection
    img_contours = cv2.findContours(edges.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    img_contours = imutils.grab_contours(img_contours)

    page_outline = None
    # iterating over all contours to find the page borders
    if len(img_contours) > 0:
        img_contours = sorted(img_contours, key=cv2.contourArea, reverse=True)
        for i in img_contours:
            perimeter = cv2.arcLength(i, True)
            approx = cv2.approxPolyDP(i, 0.02 * perimeter, True)
            # assuming that we found the page when the contours has 4 points
            if len(approx) == 4:
                page_outline = approx
                break
    # perspective transforming the image to birds eye view
    wrapped = four_point_transform(gray, page_outline.reshape(4, 2))
    # applying otsu threshold to get the circles and marked circles
    otsu_thresh = cv2.threshold(wrapped, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    # getting all the contours
    img_contours = cv2.findContours(otsu_thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    img_contours = imutils.grab_contours(img_contours)
    # array of contours representing the bubbles
    question_bubble_contours = []

    # iterating over all contours
    for i in img_contours:
        (x, y, w, h) = cv2.boundingRect(i)
        # checking if the contours is a circle as for circle w/h = 1
        ar = w / float(h)
        # if w and h are > some minimum and close to a circle than assuming that contour is a bubble
        if w > - 20 and h >= 20 and 0.9 <= ar <= 1.1:
            question_bubble_contours.append(i)
    # sorting all contours from top to bottom
    question_bubble_contours = contours.sort_contours(question_bubble_contours, method="top-to-bottom")[0]
    res = 0
    # iterating over all the bubbles in groups of OPTIONS as those give the bubbles for one question for grading
    for (q, i) in enumerate(np.arange(0, len(question_bubble_contours), OPTIONS)):
        # sorting the groups of contours from left ot right
        img_contours = contours.sort_contours(question_bubble_contours[i:i + OPTIONS])[0]
        marked = None
        # iterating over those contours
        for (j, c) in enumerate(img_contours):
            # creating a mask of zeros and applying bitwise and with our threshold image to get the bubble that is
            # marked as marked bubble would have a higher non zero value
            mask = np.zeros(otsu_thresh.shape, dtype="uint8")
            cv2.drawContours(mask, [c], -1, 255, -1)

            mask = cv2.bitwise_and(otsu_thresh, otsu_thresh, mask=mask)
            total = cv2.countNonZero(mask)

            if marked is None or total > marked[0]:
                marked = (total, j)
        # comparing the marked answer ot the answer key
        k = ANSWER_KEY[q]
        # adding 1 result if the answer is correct
        if k == marked[1]:
            res += 1
    # returning result

    # Creating GUI window to display an image on screen
    # first Parameter is windows title (should be in string format)
    # Second Parameter is image array
    # cv2.imshow("image", wrapped)

    # To hold the window on screen, we use cv2.waitKey method
    # Once it detected the close input, it will release the control
    # To the next line
    # First Parameter is for holding screen for specified milliseconds
    # It should be positive integer. If 0 pass an parameter, then it will
    # hold the screen until user close it.
    # cv2.waitKey(0)

    # It is for removing/deleting created GUI window from screen
    # and memory
    # cv2.destroyAllWindows()
    return res
