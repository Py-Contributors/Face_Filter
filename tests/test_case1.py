"""
Test Case 1

Test case locally for get request

"""
from manage import app


def test_app():
    """ Test case for get Request """
    response = app.test_client().get("/")

    assert response.status_code == 200
    assert type(response.data) == bytes

    """ Test case for face detection version 1 """
    response = app.test_client().get("api/v1/facedetection")

    assert response.status_code == 200
    assert type(response.data) == bytes

    """ Test case for face detection version 2 """
    response = app.test_client().get("api/v2/facedetection")

    assert response.status_code == 200
    assert type(response.data) == bytes

    """ Test case for Face Filter Version 1 """
    response = app.test_client().get("api/v1/facefilter")

    assert response.status_code == 200
    assert type(response.data) == bytes

    """ Test case for get image """
    response = app.test_client().get("/uploads/sample.jpg")

    assert response.status_code == 200
    assert type(response.data) == bytes

    """ Test case for show command """
    response = app.test_client().get("/command/show")

    assert response.status_code == 200
    assert type(response.data) == bytes

    """ Test Case for delete command """
    response = app.test_client().get("/command/delete")

    assert response.status_code == 200
    assert type(response.data) == bytes
