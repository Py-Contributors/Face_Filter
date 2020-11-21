import os
import imghdr
import cv2
from datetime import datetime
from PIL import Image
from flask import Flask, request, jsonify, send_file
from werkzeug.utils import secure_filename

from settings import BASE_DIR, make_folder
from settings import title, base_url, api_version
from utils import faceFilter, faceDetection, faceDetectionDNN

app = Flask(__name__)

# create folder for uploading image
make_folder("uploads")
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")

# app configurations
app.config["MAX_CONTENT_LENGTH"] = 1024 * 1024 * 50
app.config["UPLOAD_EXTENSIONS"] = [".jpg", ".png", ".jpeg"]
app.config["JSON_SORT_KEYS"] = False


# validating file contents
def validate_image(stream):
    header = stream.read(512)
    stream.seek(0)
    format = imghdr.what(None, header)
    if not format:
        return None
    return "." + (format if format != "jpeg" else "jpg")


@app.errorhandler(413)
def too_large(e):
    return "File is too large", 413


""" OpenCV FaceFilter RestAPI """
@app.route("/", methods=["GET"])
def home():
    return jsonify(
        {
            "title": title,
            "api_version": api_version,
            "documentation": "documentation_url",
            "face_filter_url": f"{base_url}/facefilter",
            "face_detection_url": f"{base_url}/facedetection",
            "Author": "Deepak Raj",
            "github": "https://github.com/codeperfectplus",
            "email": "deepak008@live.com",
            "image_retain_policy": "Image will not use in any purpose. It will be delete from server in some time. So Save your Output image.",
            "supported_image_type": "{Jpg, Png}",
            "time": datetime.now(),
        }
    )


""" Face Detection Post Request
Input post request:
    file: image_file
output:
    detected face and number of face """


@app.route("/facedetection", methods=["GET", "POST"])
def face_detection():
    if request.method == "POST":
        upload_file = request.files["file"]
        filename = secure_filename(upload_file.filename)
        if filename != "":
            file_ext = os.path.splitext(filename)[1]
            if file_ext not in app.config[
                "UPLOAD_EXTENSIONS"
            ] or file_ext != validate_image(upload_file.stream):
                return "Invalid Image", 400

            image_path = "/".join([UPLOAD_DIR, filename])

            upload_file.save(image_path)

            preprocess_img = faceDetectionDNN(image_path)
            # change BGR image RGb
            preprocess_img = cv2.cvtColor(preprocess_img, cv2.COLOR_BGR2RGB)
            output_image = Image.fromarray(preprocess_img, "RGB")
            output_image.save(image_path)

            return jsonify(
                {
                    "title": title,
                    "api_version": api_version,                    
                    "file_name": filename,
                    "output_image_url": f"{base_url}/uploads/{filename}",
                    "image_retain_policy": "Image will not use in any purpose. It will be delete from server in some time. So Save your Output image.",
                    "time": datetime.now(),
                }
            )
    return jsonify(
        {
            "title": title,
            "API Version": api_version,
            "status": "Create post request for face-detection",
            "docs": "docs_url",
        }
    )


""" Face Filter post request.
input post:
    file: image_file
    mask: num:<1-3> """


@app.route("/facefilter", methods=["GET", "POST"])
def face_filter():
    if request.method == "POST":
        upload_file = request.files["file"]
        mask_num = request.form["mask"]

        filename = secure_filename(upload_file.filename)
        if filename != "":
            file_ext = os.path.splitext(filename)[1]
            if file_ext not in app.config[
                "UPLOAD_EXTENSIONS"
            ] or file_ext != validate_image(upload_file.stream):
                return "Invalid Image", 400

            image_path = "/".join([UPLOAD_DIR, filename])

            upload_file.save(image_path)

            preprocess_image = faceFilter(image_path, mask_num)
            preprocess_image = cv2.cvtColor(preprocess_image, cv2.COLOR_BGR2RGB)
            output_image = Image.fromarray(preprocess_image, "RGB")
            output_image.save(image_path)

            return jsonify(
                {
                    "title": title,
                    "api_version": api_version,
                    "file_name": filename,
                    "output_image_url": f"{base_url}/uploads/{filename}",
                    "image_retain_policy": "Image will not use in any purpose. It will be delete from server in some time. So Save your Output image.",
                    "time": datetime.now(),
                }
            )
    return jsonify(
        {
            "title": title,
            "API Version": api_version,
            "status": "Create post request for face-filters",
            "docs": "docs_url",
        }
    )


# methods for output_image_url
@app.route("/uploads/<image_dest>")
def get_img(image_dest):
    return send_file(f"uploads/{image_dest}")

