import os
import requests

from settings import ASSETS_DIR


def test_app():
    # test for get request
    response = requests.get("http://opencv-api.herokuapp.com/")

    assert response.status_code == 200
    assert type(response.json()) == dict

    # Face Detection version 1
    response = requests.get("http://opencv-api.herokuapp.com/api/v1/facedetection")

    assert response.status_code == 200
    assert type(response.json()) == dict

    file_path = os.path.join(ASSETS_DIR, "sample.jpg")
    files = {"file": open(file_path, "rb")}
    response = requests.post(
        "http://opencv-api.herokuapp.com/api/v1/facedetection", files=files
    )

    assert response.status_code == 200
    assert type(response.json()) == dict

    # Face Detection version 2
    response = requests.get("http://opencv-api.herokuapp.com/api/v2/facedetection")

    assert response.status_code == 200
    assert type(response.json()) == dict

    file_path = os.path.join(ASSETS_DIR, "sample.jpg")
    files = {"file": open(file_path, "rb")}
    response = requests.post(
        "http://opencv-api.herokuapp.com/api/v2/facedetection", files=files
    )

    assert response.status_code == 200
    assert type(response.json()) == dict

    # Face Filter version 1
    response = requests.get("http://opencv-api.herokuapp.com/api/v1/facefilter")

    assert response.status_code == 200
    assert type(response.json()) == dict

    file_path = os.path.join(ASSETS_DIR, "sample2.jpg")
    files = {
        "file": open(file_path, "rb"),
    }
    data = {"mask": 1}
    response = requests.post(
        "http://opencv-api.herokuapp.com/api/v1/facefilter", files=files, data=data
    )

    assert response.status_code == 200
    assert type(response.json()) == dict

    # get request test for access files
    response = requests.get("http://opencv-api.herokuapp.com/uploads/sample.jpg")

    assert response.status_code == 200

    # test for show command
    response = requests.get("http://opencv-api.herokuapp.com/command/show")

    assert response.status_code == 200
    assert type(response.json()) == dict