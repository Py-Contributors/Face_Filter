""" test script locally """
import os
import requests

from settings import BASE_DIR

# chnage it to facefilter for facefilter test
post_request = 'facedetection'

if post_request == 'facefilter':
    
    url = "https://opencv-api.herokuapp.com/facefilter"

    file_path = os.path.join(BASE_DIR, 'assets/sample.jpg')
    files = {
        "file": open(file_path, "rb"),
    }
    data = {"mask": 1}
    response = requests.post(url, files=files, data=data)
    print("Respone: ", response.status_code)
    print(response.json())

if post_request == 'facedetection':

    url = "https://opencv-api.herokuapp.com/facedetection"

    file_path = os.path.join(BASE_DIR, 'assets/sample2.jpg')
    files = {
        "file": open(file_path, "rb"),
    }
    response = requests.post(url, files=files)
    print("Respone: ", response.status_code)
    print(response.json())