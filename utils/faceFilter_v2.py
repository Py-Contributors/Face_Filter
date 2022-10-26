"""
Face Detection V2

Classifier Type :
    deploy.prototxt.txt
    res10_300x300_ssd_iter_140000

Output :
    Image with rectangle mark on face
"""

import os
import numpy as np
import cv2

from utils.apply_mask import applyMask
from settings import ASSETS_DIR


# Global Declarations
proto = os.path.join(ASSETS_DIR, "deploy.prototxt.txt")
model = os.path.join(ASSETS_DIR, "res10_300x300_ssd_iter_140000.caffemodel")
confThresh = 0.8
net = cv2.dnn.readNetFromCaffe(proto, model)


async def faceFilterv2(imgPath, mask_num):
    """
    FaceFilter V2 using OpenCV DNN

    Args:
        imgPath (str): Path to image
        mask_num (int): Mask number to apply

    Returns:
        img (numpy.ndarray): Image with mask applied
    """
    img = cv2.imread(imgPath)

    all_mask = {
        1: "filters/dog.png",
        2: "filters/cat.png",
        3: "filters/dog2.png",
    }

    mask = cv2.imread(all_mask[int(mask_num)])

    (h, w) = img.shape[:2]
    blob = cv2.dnn.blobFromImage(
        cv2.resize(img, (300, 300)), 1.0, (300, 300), (104.0, 177.0, 123.0)
    )

    net.setInput(blob)
    detections = net.forward()
    for i in range(0, detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence < confThresh:
            continue

        box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
        (startX, startY, endX, endY) = box.astype("int")

        img[startY:endY, startX:endX] = applyMask(img[startY:endY,
                                                      startX:endX], mask)

    return img
