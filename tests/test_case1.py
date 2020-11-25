from fastapi.testclient import TestClient

from manage import app

client = TestClient(app)

def test_app():
    """ Test case for get Request """
    response = client.get("/")

    assert response.status_code == 200
    assert type(response.json()) == dict

    """ Test case for face detection version 1 """
    response = client.get("api/v1/facedetection")

    assert response.status_code == 200
    assert type(response.json()) == dict

    """ Test case for face detection version 2 """
    response = client.get("api/v2/facedetection")

    assert response.status_code == 200
    assert type(response.json()) == dict

    """ Test case for Face Filter Version 1 """
    response = client.get("api/v1/facefilter")

    assert response.status_code == 200
    assert type(response.json()) == dict

    """ Test case for get image """
    response = client.get("/uploads/sample.jpg")

    assert response.status_code == 200
    #assert type(response.json()) == bytes

    """ Test case for show command """
    response = client.get("/command/show")

    assert response.status_code == 200
    assert type(response.json()) == dict

    """ Test Case for delete command """
    response = client.get("/command/delete")

    assert response.status_code == 200
    assert type(response.json()) == dict

