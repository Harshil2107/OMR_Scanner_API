from __future__ import print_function
import requests
import json
import cv2
addr = 'http://localhost:5000'
test_url = addr + '/api/setkey'

content_type ="application/json"
headers = {'content-type': content_type}
ans = {0:0, 1:0, 2:0, 3:0, 4:0}
response = requests.post(test_url, json=ans, headers=headers)
print(response.text)


test_url = addr + '/api/gradeomr'

# prepare headers for http request
content_type = 'image/jpeg'
headers = {'content-type': content_type}

img = cv2.imread('images/omr_test_02.png')
# encode image as jpeg
_, img_encoded = cv2.imencode('.png', img)
# send http request with image and receive response
response = requests.post(test_url, data=img_encoded.tobytes(), headers=headers)
# decode response
print(response.text)


