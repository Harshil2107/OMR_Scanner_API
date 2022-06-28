from __future__ import print_function

import json

import cv2
import requests


def set_anskey(ans):
    addr = 'http://localhost:5000'
    test_url = addr + '/api/setkey'

    content_type = "application/json"
    headers = {'content-type': content_type}
    response = requests.post(test_url, json=ans, headers=headers)


def grade_img(url):
    addr = 'http://localhost:5000'
    test_url = addr + '/api/gradeomr'

    # prepare headers for http request
    content_type = 'image/jpeg'
    headers = {'content-type': content_type}

    img = cv2.imread(url)
    # encode image as jpeg
    _, img_encoded = cv2.imencode('.png', img)
    # send http request with image and receive response
    response = requests.post(test_url, data=img_encoded.tobytes(), headers=headers)
    # decode response
    ans = json.loads(response.text)
    return ans['correct']
