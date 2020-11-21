import os
import requests

from settings import ASSETS_DIR
from settings import base_url

# chnage it to facefilter for facefilter test
post_request = 'facedetection'

if post_request == 'facefilter':
    
    url = f"{base_url}/facefilter"

    file_path = os.path.join(ASSETS_DIR, 'sample.jpg')
    files = {
        "file": open(file_path, "rb"),
    }
    data = {"mask": 1}
    response = requests.post(url, files=files, data=data)
    print("Respone: ", response.status_code)
    print(response.json())

if post_request == 'facedetection':

    url = f"{base_url}/facedetection"

    file_path = os.path.join(ASSETS_DIR, 'sample2.jpg')
    files = {
        "file": open(file_path, "rb"),
    }
    response = requests.post(url, files=files)
    print("Respone: ", response.status_code)
    print(response.json())