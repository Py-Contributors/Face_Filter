"""
extra settings for flask api configurations
"""

import os
import shutil
from pathlib import Path
from datetime import datetime
from os.path import isdir, join as joinpath

BASE_DIR = Path(__file__).resolve().parent

UPLOADS_DIR = joinpath(BASE_DIR, "uploads")
ASSETS_DIR = joinpath(BASE_DIR, "assets")
FILTERS_DIR = joinpath(BASE_DIR, "filters")

def create_directory(folder_name):
    """ Create new directory """
    if not isdir(folder_name):
        os.mkdir(folder_name)


def recreate_uploads_dir():
    """ Recreate the entire uploads directory """
    try:
        shutil.rmtree(joinpath(UPLOADS_DIR)),
    except Exception as error:
        print(error)
    create_directory("uploads")
    try:
        shutil.copy(
            joinpath(ASSETS_DIR, "sample.jpg"), joinpath(UPLOADS_DIR, "sample.jpg")
        )
    except Exception as error:
        print(error)

# creaing uploads directry
create_directory('uploads')

""" Json data """
title = "OpenCV Rest API with FastAPI for Face Detection and Face Filters"
api_version = "0.0.2-alpha"
base_url = "https://opencv-api.herokuapp.com"
documentation_url = "https://opencv-api.herokuapp.com/docs"
current_time = datetime.utcnow()
num_of_image_on_server = len(os.listdir(UPLOADS_DIR))


