from os.path import join as joinpath
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import FileResponse
import shutil
import cv2
from PIL import Image
import os

import settings
from settings import UPLOADS_DIR,base_url
from utils import faceDetectionv1, faceDetectionv2, faceFilterv1

app = FastAPI()

@app.get("/")
async def home():
    """ OpenCV FaceFilter RestAPI"""
    return (
        {
            "title": settings.title,
            "api_version": settings.api_version,
            "documentation": f"{settings.documentation_url}",
            "face_filter_v1": f"{base_url}/api/v1/facefilter",
            "face_detection_v1": f"{base_url}/api/v1/facedetection",
            "face_detection_v2": f"{base_url}/api/v2/facedetection",
            "author": "Deepak Raj",
            "github": "https://github.com/codeperfectplus",
            "email": "deepak008@live.com",
            "image_retain_policy": "Image will not use in any purpose. It will be delete from server in some time. So Save your Output image.",
            "supported_image_type": "{Jpg, Png}",
            "time": settings.current_time,
            "total_image_on_server": settings.num_of_image_on_server,
        }
    )

@app.get('/api/v1/facedetection')
async def face_detection_version_1_get():
    return (
        {
            "title": "Face Detection Version 1",
            "API Version": settings.api_version,
            "status": "Create post request for face-detection",
            "documentation": f"{settings.documentation_url}",
        }
    )

@app.post('/api/v1/facedetection')
async def face_detection_version_1(image: UploadFile = File(...)):
    filename = image.filename
    image_path = joinpath(UPLOADS_DIR, filename)
    with open(image_path, 'wb') as buffer:           
        shutil.copyfileobj(image.file, buffer)
    
    preprocess_img, _= faceDetectionv1(image_path)
    # change BGR image RGb
    preprocess_img = cv2.cvtColor(preprocess_img, cv2.COLOR_BGR2RGB)
    output_image = Image.fromarray(preprocess_img, "RGB")
    output_image.save(image_path)

    return {
                "title": settings.title,
                "api_version": settings.api_version,
                "file_name": filename,
                "output_image_url": f"{base_url}/uploads/{filename}",
                "image_retain_policy": "Image will not use in any purpose. It will be delete from server in some time. So Save your Output image.",
                "time": settings.current_time,
                "documentation": f"{settings.documentation_url}",
            }

@app.get('/api/v2/facedetection')
async def face_detection_version_2_get():
    return (
        {
            "title": "Face Detection Version 2",
            "API Version": settings.api_version,
            "status": "Create post request for face-detection",
            "documentation": f"{settings.documentation_url}",
        }
    )

@app.post('/api/v2/facedetection')
async def face_detection_version_2(image: UploadFile = File(...)):
    filename = image.filename
    image_path = joinpath(UPLOADS_DIR, filename)
    with open(image_path, 'wb') as buffer:           
        shutil.copyfileobj(image.file, buffer)
    
    preprocess_img= faceDetectionv2(image_path)
    # change BGR image RGb
    preprocess_img = cv2.cvtColor(preprocess_img, cv2.COLOR_BGR2RGB)
    output_image = Image.fromarray(preprocess_img, "RGB")
    output_image.save(image_path)

    return {
                "title": settings.title,
                "api_version": settings.api_version,
                "file_name": filename,
                "output_image_url": f"{base_url}/uploads/{filename}",
                "image_retain_policy": "Image will not use in any purpose. It will be delete from server in some time. So Save your Output image.",
                "time": settings.current_time,
                "documentation": f"{settings.documentation_url}",
            }

@app.get('/api/v1/facefilter')
async def face_filter_version_1_get():
    return (
        {
            "title": "Face Detection Version 1",
            "API Version": settings.api_version,
            "status": "Create post request for face-detection",
            "documentation": f"{settings.documentation_url}",
        }
    )
    
@app.post('/api/v1/facefilter')
async def face_filter_version_1(image: UploadFile = File(...), mask_num: int=Form(...)):
    filename = image.filename
    image_path = joinpath(UPLOADS_DIR, filename)
    with open(image_path, 'wb') as buffer:           
        shutil.copyfileobj(image.file, buffer)
    
    preprocess_img= faceFilterv1(image_path, mask_num)
    # change BGR image RGb
    preprocess_img = cv2.cvtColor(preprocess_img, cv2.COLOR_BGR2RGB)
    output_image = Image.fromarray(preprocess_img, "RGB")
    output_image.save(image_path)

    return {
                "title": settings.title,
                "api_version": settings.api_version,
                "file_name": filename,
                "output_image_url": f"{base_url}/uploads/{filename}",
                "image_retain_policy": "Image will not use in any purpose. It will be delete from server in some time. So Save your Output image.",
                "time": settings.current_time,
                "documentation": f"{settings.documentation_url}",
            }

@app.get('/uploads/{image_dest}')
async def get_img_from_server(image_dest):
    return FileResponse(f"uploads/{image_dest}")

@app.get("/uploads/{image_dest}/delete")
async def delete_image_from_server(image_dest):
    """ Delete image from serer  """
    try:
        os.remove(joinpath(UPLOADS_DIR, image_dest))
    except Exception as error:
        print(error)
    return ({"file_name": image_dest, "delete_it_from_server": True})


@app.get("/command/delete")
async def delete_dir_from_server():
    """recreating uploads dir and copying smaple.jpg file again.
    sample.jpg is for pytest purpose.
    """
    settings.recreate_uploads_dir()
    return ({"status": "clearning uploads folder"})


@app.get("/command/show")
async def show_dir_status():
    """ Show content of uploads dir """
    image_name = os.listdir(UPLOADS_DIR)
    return (
        {"total_image": settings.num_of_image_on_server, "image_name": image_name}
    )


""" empty the uploads dir if total no. of image is more than 50. """
if settings.num_of_image_on_server > 50:
    settings.recreate_uploads_dir()