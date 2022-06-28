import cv2
import numpy as np
from flask import Flask, request, Response

from scanner import *

# Initialize the Flask application
app = Flask(__name__)


# route http posts to this method
@app.route('/api/gradeomr', methods=['POST'])
def gradeomr():
    r = request
    # convert string of image data to uint8
    nparr = np.fromstring(r.data, np.uint8)
    # decode image
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    res = grade_omr(img)

    return {'correct': res}


@app.route('/api/setkey', methods=['POST'])
def setkey():
    r = request.get_json()
    key = {}
    k = 0
    for i in r:
        key[k] = r[i]
        k += 1
    set_anskey(key)
    return {'key': r}


# start flask app
if __name__ == '__main__':
    app.debug = True
    app.run(host='127.0.0.1', port=5000)
