""" Test Case 4

Test case for Heroku Post request
 """
import os
import requests

from settings import ASSETS_DIR, base_url

file_path = os.path.join(ASSETS_DIR, "sample.jpg")


def test_app():

    """ Test case for face detection version 1 """
    files = {"file": open(file_path, "rb")}
    response = requests.post(f"{base_url}/api/v1/facedetection", files=files)

    assert response.status_code == 200
    assert type(response.json()) == dict

    """ Face case for face detection version 2 """
    files = {"file": open(file_path, "rb")}
    response = requests.post(f"{base_url}/api/v2/facedetection", files=files)

    assert response.status_code == 200
    assert type(response.json()) == dict

    """ Test case for face filter version 1 """

    files = {
        "file": open(file_path, "rb"),
    }
    data = {"mask": 1}
    response = requests.post(f"{base_url}/api/v1/facefilter", files=files, data=data)

    assert response.status_code == 200
    assert type(response.json()) == dict
