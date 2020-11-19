#!/home/inspiron3551/anaconda3/bin/python
import os
import numpy as np
from flask import Flask, jsonify, request, redirect, send_file, url_for, render_template
from PIL import Image
import cv2
import pickle

from facefilter import main
from face_detection import detectedFace
from utils import randomFilename

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

""" 
OpenCV FaceFilter RestAPI
"""
@app.route('/', methods=['GET'])
def home():
    return jsonify(
        {
        'title': 'OpenCV REST API with Flask',
        'face filter': url_for('face_filter'),
        'face detection': url_for('face_detection'),
        'github': 'https://github.com/codeperfectplus',
        'documentation': 'documentation_url',
        'author': 'Deepak Raj'
        }
    )        

'''
Face Filter post request.
input post;
    file: image_file
    mask: num:<1-3>
'''
@app.route('/facefilter', methods=['GET', 'POST'])
def face_filter():

    if request.method == 'POST':
        try:
            os.mkdir('media')
        except Exception:
            print('Folder already exists')

        media_root = os.path.join(BASE_DIR, 'media')
        upload_image = request.files.getlist('file')[0]
        mask_num = request.form["mask"]

        image_name = upload_image.filename

        image_path = "/".join([media_root, image_name])
        
        # saving input image to server
        upload_image.save(image_path)

        # main() function is for apply mask on image
        preprocess_image = main(image_path, mask_num)
        output_image = Image.fromarray(preprocess_image, 'RGB')
        output_image.save(image_path)

        return jsonify(
            {
                'output_image': image_path,
                'file_name': image_name
            }
        )
    return jsonify({'status': 'Create post request for face-filters'})

'''
Face Detection Post Request

Input post request:
    file: image_file
output:
    detected face and number of face
'''
@app.route('/facedetection', methods=['GET','post'])
def face_detection():

    if request.method == 'POST':
        media_root = os.path.join(BASE_DIR, 'media')
        upload_image = request.files.getlist('file')[0]

        image_name = upload_image.filename

        image_path = "/".join([media_root, image_name])
        
        # saving input image to server
        upload_image.save(image_path)
        
        preprocess_img, num_of_faces = detectedFace(image_path)
        output_image = Image.fromarray(preprocess_img, 'RGB')
        output_image.save(image_path)

        return jsonify(
            {
                'Total detected face': num_of_faces,
                'output_image': image_path,
                'file_name': image_name
            }
        )
    return jsonify({'status': 'Create post request for face-detection'})


''' This is only for debugging and testing purpose'''
@app.route('/test', methods=['post'])
def test():

    media_root = os.path.join(BASE_DIR, 'media')
    upload_image = request.files['file']
    upload_image = Image.open(upload_image.stream)
    print(upload_image)
    image_name = f'{randomFilename()}.jpeg'
    image_path = "/".join([media_root, image_name])

    upload_image.save(image_path)

    img, num_face = detectedFace(image_path)
    output_image = Image.fromarray(img, 'RGB')
    output_image.save(image_path)
    

    return jsonify({'status': True})