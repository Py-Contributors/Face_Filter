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
    response =client.post("/api/v1/facedetection/",
    files={
        "file": open(file_path, 'rb')
    },
    )
    response.status_code == 200
    response.json() == dict

    response =client.post("/api/v2/facedetection/",
    files={
        "file": open(file_path, 'rb')
    },
    )
    response.status_code == 201
    response.json() == dict

    response =client.post("/api/v1/facefilter/",
    data={"mask": 1},
    files={
        "file": open(file_path, 'rb')
    },
    )
    response.status_code == 201
    response.json() == dict
