"""
Test Case 3
Test Case for Heroku GET request
"""
import requests

from settings import base_url


def test_app():
    # test for get request
    response = requests.get(f"{base_url}")

    assert response.status_code == 200
    assert type(response.json()) == dict

    # Face Detection version 1
    response = requests.get(f"{base_url}/api/v1/facedetection")

    assert response.status_code == 200
    assert type(response.json()) == dict

    # Face Detection version 2
    response = requests.get(f"{base_url}/api/v2/facedetection")

    assert response.status_code == 200
    assert type(response.json()) == dict

    # Face Filter version 1
    response = requests.get(f"{base_url}/api/v1/facefilter")

    assert response.status_code == 200
    assert type(response.json()) == dict

    # get request test for access files
    response = requests.get(f"{base_url}/uploads/sample.jpg")

    assert response.status_code == 200

    # test for show command
    response = requests.get(f"{base_url}/command/show")

    assert response.status_code == 200
    assert type(response.json()) == dict
