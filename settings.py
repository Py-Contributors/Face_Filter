import os
import string
import random

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOADS_DIR = os.path.join(BASE_DIR, "uploads")
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
FILTERS_DIR = os.path.join(BASE_DIR, "filters")

title = "OpenCV Rest API with Flask for Face Detection and Face Filters"
api_version = "0.0.1-alpha"
base_url = "https://opencv-api.herokuapp.com"
documentation_url = "documentation_url"

# create folder in root dir
def make_folder(folder_name):
    try:
        os.mkdir(folder_name)
    except Exception:
        print("folder already exists")



