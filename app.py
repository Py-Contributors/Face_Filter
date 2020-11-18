#!/home/inspiron3551/anaconda3/bin/python
import os
from flask import Flask, jsonify, request
from PIL import Image

from facefilter import main

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

@app.route('/', methods=['GET'])
def home():
    return jsonify(
        {'title': 'OpenCV REST API with Flask',
        'face_filter': 'face_filter_url',
        'face_detection': 'face_detection_url',
        'github': 'https://github.com/codeperfectplus',
        'documentation': 'documentation_url'
        })

@app.route('/face_filter', methods=['POST'])
def handleUpload():

    try:
        os.mkdir('media')
    except Exception:
        print('Folder already exists')

    target = os.path.join(BASE_DIR, 'media')
    image = request.files.getlist('file')[0]
    image_name = image.filename

    destination = "/".join([target, image_name])
    
    # saving input image to server
    image.save(destination)

    img = main(destination)
    img = Image.fromarray(img, 'RGB')
    img.save(destination)

    return jsonify({
        'Image Saved': True,
        'Image_path': destination
        })
