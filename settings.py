import os
import string
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOADS_DIR = os.path.join(BASE_DIR, "uploads")
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
FILTERS_DIR = os.path.join(BASE_DIR, "filters")

title = "OpenCV Rest API with Flask for Face Detection and Face Filters"
api_version = "0.0.1-alpha"
base_url = "https://opencv-api.herokuapp.com"
documentation_url = "documentation_url"
current_time = datetime.utcnow()
num_of_image_on_server = len(os.listdir(UPLOADS_DIR))

# create folder in root dir
def make_folder(folder_name):
    if not os.path.isdir(folder_name):
        os.mkdir(folder_name)
