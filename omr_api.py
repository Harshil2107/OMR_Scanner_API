from flask import Flask, request, Response
from scanner import *
import jsonpickle
import numpy as np
import cv2

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
    response = {'correct': res}
    # encode response using jsonpickle
    response_pickled = jsonpickle.encode(response)

    return Response(response=response_pickled, status=200, mimetype="application/json")


@app.route('/api/setkey', methods=['POST'])
def setkey():
    r = request.get_json()
    key = {}
    k=0
    for i in r:
        key[k] = r[i]
        k+=1
    print(key)
    set_anskey(key)
    return {'key': r}


# start flask app
if __name__ == '__main__':
    app.debug = True
    app.run(host='127.0.0.1', port=5000)
