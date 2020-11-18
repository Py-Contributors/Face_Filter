#!/home/inspiron3551/anaconda3/bin/python
import os
from flask import Flask, jsonify, request, redirect, send_file, url_for
from PIL import Image
import cv2

from facefilter import main
from face_detection import detectedFace

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
        'face filter': 'face_filter_url',
        'face detection': 'face_detection_url',
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
@app.route('/facefilter', methods=['POST'])
def face_filter():

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
    preprocessed_image = main(image_path, mask_num)
    preprocessed_image = Image.fromarray(preprocessed_image, 'RGB')
    preprocessed_image.save(image_path)

    return jsonify(
        {
            'output_image': image_path,
            'file_name': image_name
        }
    )

'''
Face Detection Post Request

Input post request:
    file: image_file
output:
    detected face and number of face
'''
@app.route('/facedetection', methods=['post'])
def face_detection():

    media_root = os.path.join(BASE_DIR, 'media')
    upload_image = request.files.getlist('file')[0]

    image_name = upload_image.filename

    image_path = "/".join([media_root, image_name])
    
    # saving input image to server
    upload_image.save(image_path)

    # main() function is for apply mask on image
    preprocessed_image, num_of_faces = detectedFace(image_path)
    preprocessed_image = Image.fromarray(preprocessed_image, 'RGB')
    preprocessed_image.save(image_path)

    return jsonify(
        {
            'Total detected face': num_of_faces,
            'output_image': image_path,
            'file_name': image_name
        }
    )



''' This is only for debugging and testing purpose'''
@app.route('/test', methods=['post'])
def test():

    media_root = os.path.join(BASE_DIR, 'media')
    upload_image = request.files.getlist('file')[0]

    image_name = upload_image.filename

    image_path = "/".join([media_root, image_name])
    
    # saving input image to server
    upload_image.save(image_path)

    # main() function is for apply mask on image
    preprocessed_image, num_of_faces = detectedFace(image_path)
    preprocessed_image = Image.fromarray(preprocessed_image, 'RGB')
    preprocessed_image.save(image_path)
    

    return jsonify(
        {
            'Total detected face': num_of_faces,
            'output_image': image_path,
            'file_name': image_name,
        }
    )