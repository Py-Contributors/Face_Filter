''' test script locally '''
import requests

local_url = 'http://localhost:5000/test'
heroku_url = 'https://opencv-api.herokuapp.com/test'

file_path = '/home/inspiron3551/Downloads/Pictures/samplePicture.jpg'

files = {
    'file': open(file_path, 'rb'),
}
data = {
    'mask': 2
}
response = requests.post(heroku_url, files=files, data=data)
print('Respone: ', response)
print(response.text)
#print(response.json())