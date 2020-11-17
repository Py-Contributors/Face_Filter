import requests
from PIL import Image

image_path = '/home/inspiron3551/Downloads/Pictures/30-of-the-most-influential-and-famous-entrepreneurs-from-all-over-the-world.jpg'

url = 'http://127.0.0.1:5000/'

r = requests.post(url, data={'file': open(image_path, 'rb')})

print(r.text)
