#!/home/inspiron3551/anaconda3/bin/python
import os
from flask import Flask, jsonify, request
from PIL import Image
import cv2
from facefilter import main

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

@app.route('/', methods=['GET'])
def home():
    return jsonify(
        {'title': 'OpenCV REST API with Flask',
        'Face Filter': 'face_filter_url',
        'Face Detection': 'face_detection_url',
        'github': 'https://github.com/codeperfectplus',
        'documentation': 'documentation_url',
        'author': ' '
        })

@app.route('/facefilter', methods=['POST'])
def handleUpload():

    try:
        os.mkdir('media')
    except Exception:
        print('Folder already exists')

    target = os.path.join(BASE_DIR, 'media')
    upload_image = request.files.getlist('file')[0]
    mask_num = request.form["mask"]

    image_name = upload_image.filename

    destination = "/".join([target, image_name])
    
    # saving input image to server
    upload_image.save(destination)

    preprocessed_image = main(destination, mask_num)
    preprocessed_image = Image.fromarray(preprocessed_image, 'RGB')
    preprocessed_image.save(destination)

    return jsonify({
        'Image Saved': True,
        'Image_path': destination
        })
