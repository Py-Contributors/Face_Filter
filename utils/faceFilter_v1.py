"""
Face Filter V1

Classifier Type :
    HarrCascade Frontal Face Classifier

Output :
    Applied mask on face
"""
import os
import numpy as np
import cv2

from utils.apply_mask import applyMask
from settings import ASSETS_DIR


def faceFilterv1(input_image: str, mask_num: int):
    """ 
    Face Filter V1 using OpenCV Haar Cascade Frontal Face Classifier

    Args:
        input_image (str): Path to image
        mask_num (int): Mask number to apply
    
    Returns:
        img (numpy.ndarray): Image with mask applied
    """

    input_image = cv2.imread(input_image)

    all_mask = {
        1: "filters/dog.png",
        2: "filters/cat.png",
        3: "filters/dog2.png",
    }

    mask = cv2.imread(all_mask[int(mask_num)])

    cascade = cv2.CascadeClassifier(
        os.path.join(ASSETS_DIR, "haarcascade_frontalface_default.xml")
    )

    
    # Capture frame-by-frame
    frame_h, frame_w, _ = input_image.shape
    # Convert to black-and-white
    gray = cv2.cvtColor(input_image, cv2.COLOR_RGB2GRAY)
    blackwhite = cv2.equalizeHist(gray)
    # Detect faces by creating a rectangle around each face
    rects = cascade.detectMultiScale(
        blackwhite,
        scaleFactor=1.3,
        minNeighbors=4,
        minSize=(30, 30),
        flags=cv2.CASCADE_SCALE_IMAGE,
    )
    # Iterate over each face and apply the mask
    for x, y, w, h in rects:
        # crop a frame slightly larger than the face
        y0, y1 = int(y - 0.25 * h), int(y + 0.75 * h)
        x0, x1 = x, x + w
        # give up if the cropped frame would be out-of-bounds
        if x0 < 0 or y0 < 0 or x1 > frame_w or y1 > frame_h:
            continue
        input_image[y0:y1, x0:x1] = applyMask(input_image[y0:y1, x0:x1], mask)
    return input_image
