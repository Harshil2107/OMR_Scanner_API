from flask import Flask, request

from scanner import *

# Initialize the Flask application
app = Flask(__name__)


# route http posts to this method
@app.route('/api/grade_omr', methods=['POST'])
def gradeomr():
    key = getkey()
    opt = getoptions()
    if key is None or opt is None:
        return {'return val': -1}
    r = request
    # convert string of image data to uint8
    uint8img = np.fromstring(r.data, np.uint8)
    # decode image
    img = cv2.imdecode(uint8img, cv2.IMREAD_COLOR)
    # grading the omr
    res = grade_omr(img)
    # returning the score
    return {'return val': res}


@app.route('/api/setkey', methods=['POST'])
def setkey():
    # getting data
    r = request.get_json()
    # number of options in the questions
    num_options = r[1]
    # answer key
    ans = r[0]
    key = {}
    k = 0
    # converting answer key from format {string: int, ..} to {int:int,...}
    for i in ans:
        key[k] = ans[i]
        k += 1
    # setting answer key for future scan use
    set_anskey_num_options(key, num_options)
    return {'key': ans}


# start flask app
if __name__ == '__main__':
    app.debug = True
    app.run(host='127.0.0.1', port=5000)
