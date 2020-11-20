''' test script locally '''
import requests

local_url = 'http://localhost:8080/facefilter'
heroku_url = 'https://opencv-api.herokuapp.com/facefilter'

file_path = "/home/inspiron3551/Downloads/1ilPsIsy_400x400.jpg"
files = {
    'file': open(file_path, 'rb'),
}
data = {
    'mask': 3
}
response = requests.post(heroku_url, files=files, data=data)
print('Respone: ', response)
print(response.text)
#print(response.json())