import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

title = "OpenCV Rest API with Flask for Face Detection and Face Filters"
api_version = "0.0.1-alpha"
base_url = "https://opencv-api.herokuapp.com"


# create folder in root dir
def make_folder(folder_name):
    try:
        os.mkdir(folder_name)
    except Exception:
        print("folder already exists")
