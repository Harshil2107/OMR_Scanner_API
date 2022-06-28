from call_post_methods import *

# setting up answer key {question: correct option, ...} correct option is 0 for A, 1 for B and so on
ans = {1: 1, 2: 4, 3: 0, 4: 2, 5: 1}
print(ans)
set_anskey_numoption(ans, 5)
# iterating over the testimages to grade them and printng the result
for i in range(1, 6):
    res = grade_img('images/omr_test_0' + str(i) + '.png')
    if res != -1:
        print('grade for ' + str(i) + ' is ' + str(res) + '/5')
    else:
        print("Answer key or number of options per question not set")
        break
