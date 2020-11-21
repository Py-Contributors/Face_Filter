""" test script locally """
import requests

local_url = "http://localhost:8080/facedetection"
heroku_url = "https://opencv-api.herokuapp.com/facedetection"

file_path = "/home/inspiron3551/Downloads/Pictures/leaders2.jpg"
files = {
    "file": open(file_path, "rb"),
}
data = {"mask": 1}
response = requests.post(local_url, files=files)
print("Respone: ", response)
print(response.text)
# print(response.json())
