import os
import imghdr
import cv2
from PIL import Image
from flask import Flask, request, jsonify, url_for, redirect, send_file
from werkzeug.utils import secure_filename

from utility import BASE_DIR, make_folder
from utils import faceFilter
from utils import faceDetection

app = Flask(__name__)

# create folder for uploading image
make_folder("uploads")
UPLOAD_DIR = os.path.join(BASE_DIR, 'uploads')

# app configurations
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024 * 50
app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png', '.jpeg']

#validating file contents
def validate_image(stream):
    header = stream.read(512)
    stream.seek(0)
    format = imghdr.what(None, header)
    if not format:
        return None
    return '.'+ (format if format != 'jpeg' else 'jpg')

@app.errorhandler(413)
def too_large(e):
    return 'File is too large', 413

""" OpenCV FaceFilter RestAPI """
@app.route('/', methods=['GET'])
def home():
    return jsonify(
        {
            'title': 'OpenCV REST API with Flask',
            'face filter': url_for('face_filter'),
            'face detection': url_for('face_detection'),
            'github': 'https://github.com/codeperfectplus',
            'documentation': 'documentation_url',
            'author': ''
        }
    )  

''' Face Detection Post Request
Input post request:
    file: image_file
output:
    detected face and number of face '''
@app.route('/facedetection', methods=['GET', 'POST'])
def face_detection():
    if request.method == 'POST':
        upload_file = request.files['file']
        filename = secure_filename(upload_file.filename)
        if filename != '':
            file_ext = os.path.splitext(filename)[1]
            if file_ext not in app.config["UPLOAD_EXTENSIONS"] or \
                file_ext != validate_image(upload_file.stream):
                return "Invalid Image", 400
            
            image_path = "/".join([UPLOAD_DIR, filename])

            upload_file.save(image_path)

            preprocess_img, num_of_faces = faceDetection(image_path)
            # change BGR image RGb
            preprocess_image = cv2.cvtColor(preprocess_image, cv2.COLOR_BGR2RGB)
            output_image = Image.fromarray(preprocess_img, 'RGB')
            output_image.save(image_path)

            return jsonify(
                {
                    'Total detected face': num_of_faces,
                    'output_image': image_path,
                    'file_name': filename
                }
            )
    return jsonify(
        {
            'status': 'Create post request for face-detection'
        }
    )

''' Face Filter post request.
input post:
    file: image_file
    mask: num:<1-3> '''

@app.route('/facefilter', methods=['GET', 'POST'])
def face_filter():
    if request.method == 'POST':
        upload_file = request.files['file']
        mask_num = request.form['mask']

        filename = secure_filename(upload_file.filename)
        if filename != '':
            file_ext = os.path.splitext(filename)[1]
            if file_ext not in app.config["UPLOAD_EXTENSIONS"] or \
                file_ext != validate_image(upload_file.stream):
                return "Invalid Image", 400
            
            image_path = "/".join([UPLOAD_DIR, filename])

            upload_file.save(image_path)

            preprocess_image = faceFilter(image_path, mask_num)
            preprocess_image = cv2.cvtColor(preprocess_image, cv2.COLOR_BGR2RGB)
            output_image = Image.fromarray(preprocess_image, 'RGB')
            output_image.save(image_path)

            return jsonify(
                {
                    'output_image': image_path,
                    'file_name': filename
                }
            )
    return jsonify(
        {
            'status': 'Create post request for face-filters'
        }
    )

@app.route('/test', methods=['GET', 'POST'])
def test():
    if request.method == 'POST':
        upload_file = request.files['file']
        mask_num = request.form['mask']

        filename = secure_filename(upload_file.filename)
        if filename != '':
            file_ext = os.path.splitext(filename)[1]
            if file_ext not in app.config["UPLOAD_EXTENSIONS"] or \
                file_ext != validate_image(upload_file.stream):
                return "Invalid Image", 400
            
            image_path = "/".join([UPLOAD_DIR, filename])

            upload_file.save(image_path)

            preprocess_image = faceFilter(image_path, mask_num)
            preprocess_image = cv2.cvtColor(preprocess_image, cv2.COLOR_BGR2RGB)
            output_image = Image.fromarray(preprocess_image)
            output_image.save(image_path)

            return send_file(image_path, mimetype='image/gif')

    return jsonify(
        {
            'status': 'Create post request for face-filters'
        }
    )
