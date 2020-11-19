import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def make_folder(folder_name):
    try:
        os.mkdir(folder_name)
    except Exception:
        print("folder already exists")
