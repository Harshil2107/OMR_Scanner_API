from __future__ import print_function

import json

import cv2
import requests


def set_anskey_numoption(ans, options):
    addr = 'http://localhost:5000'
    test_url = addr + '/api/setkey'
    data = [ans, options]
    content_type = "application/json"
    headers = {'content-type': content_type}
    response = requests.post(test_url, json=data, headers=headers)


def grade_img(url):
    addr = 'http://localhost:5000'
    test_url = addr + '/api/grade_omr'

    # prepare headers for http request
    content_type = 'formdata'
    headers = {'content-type': content_type}

    img = cv2.imread(url)
    # encode image as jpeg
    _, img_encoded = cv2.imencode('.png', img)
    print()
    # send http request with image and receive response
    response = requests.post(test_url, data=img_encoded.tobytes(), headers=headers)
    # decode response
    ans = json.loads(response.text)
    return ans['return val']
