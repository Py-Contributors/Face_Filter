import os
import cv2
import requests
from settings import ASSETS_DIR

pic_path = "C:/Users/inspiron/Pictures/My Picture/IMG-20210128-WA0012.jpg"


url = "localhost:5000/api/v2/facefilter"
file_path = os.path.join(ASSETS_DIR, "sample.jpg")

data = {"mask": 1}
data["file"] = open(file_path, "rb")

response = requests.post(
    "/api/v1/facefilter", data=data, content_type="multipart/form-data")

print(response)
