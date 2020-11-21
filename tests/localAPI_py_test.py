import os

from manage import app
from settings import ASSETS_DIR


def test_app():
    # test for get request
    response = app.test_client().get("/")

    assert response.status_code == 200
    assert type(response.data) == bytes

    # post request test for face detection
    file_path = os.path.join(ASSETS_DIR, "sample.jpg")

    data = {"file": open(file_path, "rb")}

    response = app.test_client().post(
        "/facedetection", data=data, content_type="multipart/form-data"
    )
    assert response.status_code == 200
    assert type(response.data) == bytes

    # post request test for face filters
    file_path = os.path.join(ASSETS_DIR, "sample2.jpg")

    data = {"mask": 1}
    data["file"] = open(file_path, "rb")

    response = app.test_client().post(
        "/facefilter", data=data, content_type="multipart/form-data"
    )
    assert response.status_code == 200
    assert type(response.data) == bytes

    # get request test for access files
    response = app.test_client().get("/uploads/sample.jpg")

    assert response.status_code == 200
    assert type(response.data) == bytes
