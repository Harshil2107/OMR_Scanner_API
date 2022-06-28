# OMR Scanner API

The API takes an image as an argument and grades the Omr provided. The API has two post requests: one that sets the answer key and the number of options per question.

## Files explaination ##

* The folder images contains test images.
* The file scanner.py has the main logic that takes the image and uses opencv and imutils to proccess the image and grade it.
* The file omr_api.py creats a basic flask server with two post request that calls the methods in scanner.py.
  * The '/api/grade_omr' is a POST request that takes image as argument and return the number of correct question or -1 if answer key or number of options are not set.
  * The '/api/setkey' is a POST request that takes an array of dictionaries with 2 elements. At index 0 is the answer key and at index 1 is the number of options.
* The file call_post_methods.py has two functions that call the respective post requests.
  * The set_anskey_numoption() calls the post request '/api/setkey'.
    * Argument - answer key and number of options.
      * answer key is defined as: {question: correct option, ...} correct option is 0 for A, 1 for B and so on. Example, ans = {1: 1, 2: 4, 3: 0, 4: 2, 5: 1}.
      * number of options is an integer.
  * the grade_img() calls the post request '/api/setkey'.
    * Argument - image path.
      * image path is dedfined as a string containing the retalive path to the image. Example, 'images/omr_test_01.png'.
    * Returns - number of correct questions or -1 if answer key or number of options are not set.
* The file main.py shows an example of how to call the above mentioned functions to grade the omr.



  
