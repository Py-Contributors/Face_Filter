''' test script locally '''
import requests

local_url = 'http://localhost:5000/facefilter'
heroku_url = 'https://snpachat-filter-restapi.herokuapp.com/facefilter'
file_path = '/home/inspiron3551/Downloads/Pictures/30-of-the-most-influential-and-famous-entrepreneurs-from-all-over-the-world.jpg'

files = {
    'file': open(file_path, 'rb'),
}

response = requests.post(heroku_url, files=files)
print(response.json())