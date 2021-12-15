"""
Main Script for GET and POST Request Route.
"""
import os
from os.path import join as joinpath
import cv2
import imghdr

from PIL import Image
from werkzeug.utils import secure_filename
from flask import Flask, request, jsonify, send_file

import settings
from settings import UPLOADS_DIR, base_url
from utils import faceDetectionv1, faceFilterv1
from utils import faceDetectionv2, faceFilterv2

app = Flask(__name__)

# create folder for uploading image
settings.create_directory("uploads")

# app configurations
app.config["DEBUG"] = False
app.config["MAX_CONTENT_LENGTH"] = 1024 * 1024 * 5
app.config["UPLOAD_EXTENSIONS"] = [".jpg", ".png", ".jpeg"]
app.config["JSON_SORT_KEYS"] = False
app.config["JSONIFY_PRETTYPRINT_REGULAR"] = True


def validate_image(stream):
    # validating file contents
    header = stream.read(512)
    stream.seek(0)
    format = imghdr.what(None, header)
    if not format:
        return None
    return "." + (format if format != "jpeg" else "jpg")


@app.errorhandler(413)
def too_large(e):
    # error handing for MAX_CONTENT_LENGTH
    return "File is too large", 413


@app.route("/", methods=["GET"])
def home():
    """ OpenCV FaceFilter RestAPI"""
    return jsonify(
        {
            "title": settings.title,
            "api_version": settings.api_version,
            "documentation": f"{settings.documentation_url}",
            "face_filter_v1": f"{base_url}/api/v1/facefilter",
            "face_detection_v1": f"{base_url}/api/v1/facedetection",
            "face_detection_v2": f"{base_url}/api/v2/facedetection",
            "Author": "Deepak Raj",
            "github": "https://github.com/codeperfectplus",
            "email": "deepak008@live.com",
            "image_retain_policy": "Image will not use in any purpose. It will be delete from server in some time. So Save your Output image.",
            "supported_image_type": "{Jpg, Png}",
            "time": settings.current_time,
            "total_image_on_server": settings.num_of_image_on_server,
        }
    )


@app.route("/api/v1/facedetection", methods=["GET", "POST"])
def face_detection_v1():
    """ Face Detection V1 """
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

            preprocess_img, _ = faceDetectionv1(image_path)
            # change BGR image RGb
            preprocess_img = cv2.cvtColor(preprocess_img, cv2.COLOR_BGR2RGB)
            output_image = Image.fromarray(preprocess_img, "RGB")
            output_image.save(image_path)

            return jsonify(
                {
                    "title": settings.title,
                    "api_version": settings.api_version,
                    "file_name": filename,
                    "output_image_url": f"{base_url}/uploads/{filename}",
                    "image_retain_policy": "Image will not use in any purpose. It will be delete from server in some time. So Save your Output image.",
                    "time": settings.current_time,
                    "documentation": f"{settings.documentation_url}",
                }
            )
    return jsonify(
        {
            "title": "Face Detection Version 1",
            "API Version": settings.api_version,
            "status": "Create post request for face-detection",
            "documentation": f"{settings.documentation_url}",
        }
    )


@app.route("/api/v1/facefilter", methods=["GET", "POST"])
def face_filter_v1():
    """ Face filter V1 """
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

            preprocess_image = faceFilterv1(image_path, mask_num)
            preprocess_image = cv2.cvtColor(preprocess_image, cv2.COLOR_BGR2RGB)
            output_image = Image.fromarray(preprocess_image, "RGB")
            output_image.save(image_path)

            return jsonify(
                {
                    "title": settings.title,
                    "api_version": settings.api_version,
                    "file_name": filename,
                    "output_image_url": f"{base_url}/uploads/{filename}",
                    "image_retain_policy": "Image will not use in any purpose. It will be delete from server in some time. So Save your Output image.",
                    "time": settings.current_time,
                    "documentation": f"{settings.documentation_url}",
                }
            )
    return jsonify(
        {
            "title": "Face Filter Version 1",
            "API Version": settings.api_version,
            "status": "Create post request for face-filters",
            "documentation": f"{settings.documentation_url}",
        }
    )


@app.route("/api/v2/facedetection", methods=["GET", "POST"])
def face_detection_v2():
    """ Face Detection version 2 """
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

            preprocess_img = faceDetectionv2(image_path)
            # change BGR image RGb
            preprocess_img = cv2.cvtColor(preprocess_img, cv2.COLOR_BGR2RGB)
            output_image = Image.fromarray(preprocess_img, "RGB")
            output_image.save(image_path)

            return jsonify(
                {
                    "title": settings.title,
                    "api_version": settings.api_version,
                    "file_name": filename,
                    "output_image_url": f"{base_url}/uploads/{filename}",
                    "image_retain_policy": "Image will not use in any purpose. It will be delete from server in some time. So Save your Output image.",
                    "time": settings.current_time,
                    "documentation": f"{settings.documentation_url}",
                }
            )
    return jsonify(
        {
            "title": "Face Detection Version 2",
            "API Version": settings.api_version,
            "status": "Create post request for face-detection",
            "documentation": f"{settings.documentation_url}",
        }
    )

@app.route("/api/v2/facefilter", methods=["GET", "POST"])
def face_filter_v2():
    """ Face filter V2 """
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

            preprocess_image = faceFilterv2(image_path, mask_num)
            preprocess_image = cv2.cvtColor(preprocess_image, cv2.COLOR_BGR2RGB)
            output_image = Image.fromarray(preprocess_image, "RGB")
            output_image.save(image_path)

            return jsonify(
                {
                    "title": settings.title,
                    "api_version": settings.api_version,
                    "file_name": filename,
                    "output_image_url": f"{base_url}/uploads/{filename}",
                    "image_retain_policy": "Image will not use in any purpose. It will be delete from server in some time. So Save your Output image.",
                    "time": settings.current_time,
                    "documentation": f"{settings.documentation_url}",
                }
            )
    return jsonify(
        {
            "title": "Face Filter Version 1",
            "API Version": settings.api_version,
            "status": "Create post request for face-filters",
            "documentation": f"{settings.documentation_url}",
        }
    )


@app.route("/uploads/<image_dest>", methods=["GET"])
def get_img(image_dest):
    """ show uploads image """
    return send_file(f"uploads/{image_dest}")


@app.route("/uploads/<image_dest>/delete", methods=["GET"])
def delete_image(image_dest):
    """ Delete image from serer  """
    try:
        os.remove(joinpath(UPLOADS_DIR, image_dest))
    except Exception as error:
        print(error)
    return jsonify({"file_name": image_dest, "delete_it_from_server": True})


@app.route("/command/delete", methods=["GET"])
def delete_dir():
    """recreating uploads dir and copying smaple.jpg file again.
    sample.jpg is for pytest purpose.
    """
    settings.recreate_uploads_dir()
    return jsonify({"status": "clearning uploads folder"})


@app.route("/command/show", methods=["GET"])
def show_dir():
    """ Show content of uploads dir """
    image_name = os.listdir(UPLOADS_DIR)
    return jsonify(
        {"total_image": settings.num_of_image_on_server, "image_name": image_name}
    )


""" empty the uploads dir if total no. of image is more than 50. """
if settings.num_of_image_on_server > 50:
    settings.recreate_uploads_dir()
