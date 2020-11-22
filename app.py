import os
import cv2
import imghdr

from PIL import Image
from werkzeug.utils import secure_filename
from flask import Flask, request, jsonify, send_file

import settings
from settings import UPLOADS_DIR, ASSETS_DIR, base_url_v1
from utils import faceFilter, faceDetectionDNN

app = Flask(__name__)

# create folder for uploading image
settings.create_directory("uploads")

# app configurations
app.config["DEBUG"] = False
app.config["MAX_CONTENT_LENGTH"] = 1024 * 1024 * 5
app.config["UPLOAD_EXTENSIONS"] = [".jpg", ".png", ".jpeg"]
app.config["JSON_SORT_KEYS"] = False
app.config["JSONIFY_PRETTYPRINT_REGULAR"] = True

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
            "title": settings.title,
            "api_version": settings.api_version,
            "documentation": f"{settings.documentation_url}",
            "face_filter_url": f"{base_url_v1}/facefilter",
            "face_detection_url": f"{base_url_v1}/facedetection",
            "Author": "Deepak Raj",
            "github": "https://github.com/codeperfectplus",
            "email": "deepak008@live.com",
            "image_retain_policy": "Image will not use in any purpose. It will be delete from server in some time. So Save your Output image.",
            "supported_image_type": "{Jpg, Png}",
            "time": settings.current_time,
            "total_image_on_server": settings.num_of_image_on_server
        }
    )


""" Face Detection Post Request
Input post request:
    file: image_file
output:
    detected face and number of face """
@app.route("/api/v1/facedetection", methods=["GET", "POST"])
def face_detection_v1():
    if request.method == "POST":
        upload_file = request.files["file"]
        filename = secure_filename(upload_file.filename)
        if filename != "":
            file_ext = os.path.splitext(filename)[1]
            if file_ext not in app.config[
                "UPLOAD_EXTENSIONS"
            ] or file_ext != validate_image(upload_file.stream):
                return "Invalid Image", 400

            image_path = "/".join([UPLOADS_DIR, filename])

            upload_file.save(image_path)

            preprocess_img = faceDetectionDNN(image_path)
            # change BGR image RGb
            preprocess_img = cv2.cvtColor(preprocess_img, cv2.COLOR_BGR2RGB)
            output_image = Image.fromarray(preprocess_img, "RGB")
            output_image.save(image_path)

            return jsonify(
                {
                    "title": settings.title,
                    "api_version": settings.api_version,
                    "file_name": filename,
                    "output_image_url": f"{base_url_v1}/uploads/{filename}",
                    "image_retain_policy": "Image will not use in any purpose. It will be delete from server in some time. So Save your Output image.",
                    "time": settings.current_time,                    
                    "documentation": f"{settings.documentation_url}",
                }
            )
    return jsonify(
        {
            "title": settings.title,
            "API Version": settings.api_version,
            "status": "Create post request for face-detection",
            "documentation": f"{settings.documentation_url}",
        }
    )


""" Face Filter post request.
input post:
    file: image_file
    mask: num:<1-3> """
@app.route("/api/v1/facefilter", methods=["GET", "POST"])
def face_filter_v1():
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

            image_path = "/".join([UPLOADS_DIR, filename])

            upload_file.save(image_path)

            preprocess_image = faceFilter(image_path, mask_num)
            preprocess_image = cv2.cvtColor(preprocess_image, cv2.COLOR_BGR2RGB)
            output_image = Image.fromarray(preprocess_image, "RGB")
            output_image.save(image_path)

            return jsonify(
                {
                    "title": settings.title,
                    "api_version": settings.api_version,
                    "file_name": filename,
                    "output_image_url": f"{base_url_v1}/uploads/{filename}",
                    "image_retain_policy": "Image will not use in any purpose. It will be delete from server in some time. So Save your Output image.",
                    "time": settings.current_time,
                    "documentation": f"{settings.documentation_url}",
                }
            )
    return jsonify(
        {
            "title": settings.title,
            "API Version": settings.api_version,
            "status": "Create post request for face-filters",
            "documentation": f"{settings.documentation_url}",
        }
    )


# methods for output_image_url
@app.route("/uploads/<image_dest>", methods=["GET"])
def get_img(image_dest):
    return send_file(
        f"uploads/{image_dest}"
    )


# delete one image only
@app.route("/uploads/<image_dest>/delete", methods=["GET"])
def delete_image(image_dest):
    try:
        os.remove(os.path.join(UPLOADS_DIR, image_dest))
    except:
        print("shutil error! while deleting the image")
    return jsonify(
        {
            "file_name": image_dest, 
            "delete_it_from_server": True
        }
    )


# methods for empty the uploads dir
@app.route("/command/delete", methods=["GET"])
def delete_dir():
    """ recreating uploads dir and copying smaple.jpg file again. 
    It's for pytest purpose in both dir.
     """
    settings.recreate_uploads_dir()
    return jsonify(
        {
            "status": "clearning uploads folder"
        }
    )

# methods for show contents of entire uploads dir
@app.route("/command/show", methods=["GET"])
def show_dir():
    image_name = os.listdir(UPLOADS_DIR)
    return jsonify(
        {
            "total_image": settings.num_of_image_on_server,
            "image_name": image_name
        }
    )

# empty the uploads dir if total no. of image is more than 100.
if settings.num_of_image_on_server > 50:
    settings.recreate_uploads_dir()
