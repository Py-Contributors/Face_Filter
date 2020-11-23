"""
Test Case 2

Test Case Locally for post request
"""
import os

from manage import app
from settings import ASSETS_DIR

file_path = os.path.join(ASSETS_DIR, "sample.jpg")


def test_app():
    """ Test case for Face Detection version 1 """
    data = {"file": open(file_path, "rb")}
    response = app.test_client().post(
        "api/v1/facedetection", data=data, content_type="multipart/form-data"
    )
    assert response.status_code == 200
    assert type(response.data) == bytes

    """ Test case for face detection version 2 """
    data = {"file": open(file_path, "rb")}

    response = app.test_client().post(
        "api/v2/facedetection", data=data, content_type="multipart/form-data"
    )
    assert response.status_code == 200
    assert type(response.data) == bytes

    """ Test case for face filter version 1 """
    data = {"mask": 1}
    data["file"] = open(file_path, "rb")

    response = app.test_client().post(
        "/api/v1/facefilter", data=data, content_type="multipart/form-data"
    )
    assert response.status_code == 200
    assert type(response.data) == bytes
