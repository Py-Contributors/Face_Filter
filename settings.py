import os
import string
from datetime import datetime
import shutil

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOADS_DIR = os.path.join(BASE_DIR, "uploads")
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
FILTERS_DIR = os.path.join(BASE_DIR, "filters")

title = "OpenCV Rest API with Flask for Face Detection and Face Filters"
api_version = "0.0.2-alpha"
base_url_v1 = "https://opencv-api.herokuapp.com/api/v1"
documentation_url = "https://opencv-api.readthedocs.io/"
current_time = datetime.utcnow()
num_of_image_on_server = len(os.listdir(UPLOADS_DIR))

# create directory in the root dir
def create_directory(folder_name):
    if not os.path.isdir(folder_name):
        os.mkdir(folder_name)


# empty the uploads dir and recretae it
def recreate_uploads_dir():
    try:
        shutil.rmtree(os.path.join(UPLOADS_DIR)),
    except Exception:
        print(Exception)
    create_directory("uploads")
    try:
        shutil.copy(
            os.path.join(ASSETS_DIR, "sample.jpg"),
            os.path.join(UPLOADS_DIR, "sample.jpg")
        )
    except Exception:
        print(Exception)
