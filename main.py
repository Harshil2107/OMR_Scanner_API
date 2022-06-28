from test import *

ans = {1: 1, 2: 4, 3: 0, 4: 2, 5: 1}
print(ans)
set_anskey(ans)

for i in range(1, 6):
    res = grade_img('images/omr_test_0' + str(i) + '.png')
    print('grade for ' + str(i) + ' is ' + str(res) + '/5')
