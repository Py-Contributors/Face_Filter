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
    pass