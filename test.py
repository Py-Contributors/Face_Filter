''' test script locally '''
import requests

file_path = '/home/inspiron3551/Downloads/Pictures/30-of-the-most-influential-and-famous-entrepreneurs-from-all-over-the-world.jpg'

files = {
    'file': open(file_path, 'rb'),
}

response = requests.post('http://localhost:5000/facefilter', files=files)
print(response.json())