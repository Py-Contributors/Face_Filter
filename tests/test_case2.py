"""
Test Case 2

Test Case Locally for post request
"""
import os
from fastapi.testclient import TestClient

from manage import app
from settings import ASSETS_DIR

client = TestClient(app)

file_path = os.path.join(ASSETS_DIR, "sample.jpg")


def test_app():
    """ Test case for Face Detection version 1 """
    data = {"file": open(file_path, "rb")}
    response = client.post(
        "api/v1/facedetection", data=data)
    assert response.status_code == 200
    assert type(response.data) == bytes