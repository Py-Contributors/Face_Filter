''' test script locally '''
import requests

local_url = 'http://localhost:5000/test'
heroku_url = 'https://opencv-api.herokuapp.com/facefilter'

file_path = "/home/inspiron3551/Downloads/Pictures/30-of-the-most-influential-and-famous-entrepreneurs-from-all-over-the-world.jpg"

files = {
    'file': open(file_path, 'rb'),
}
data = {
    'mask': 3
}
response = requests.post(local_url, files=files, data=data)
print('Respone: ', response)
print(response.text)
#print(response.json())