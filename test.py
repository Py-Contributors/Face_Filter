""" test script locally """
import requests

local_url = "http://localhost:8080/facefilter"
heroku_url = "https://opencv-api.herokuapp.com/facefilter"

file_path = "/home/inspiron3551/Downloads/Pictures/564ce7fd2491f990008b6498.jpeg"
files = {
    "file": open(file_path, "rb"),
}
data = {"mask": 1}
response = requests.post(local_url, files=files, data=data)
print("Respone: ", response)
print(response.text)
# print(response.json())
