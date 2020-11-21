import os
import numpy as np
import cv2

from settings import ASSETS_DIR

# Global Declarations
proto = os.path.join(ASSETS_DIR, 'deploy.prototxt.txt')
model=os.path.join(ASSETS_DIR, 'res10_300x300_ssd_iter_140000.caffemodel')
confThresh=0.8
net = cv2.dnn.readNetFromCaffe(proto, model)

def faceDetectionDNN(imgPath):
    img = cv2.imread(imgPath)

    (h, w) = img.shape[:2]
    blob = cv2.dnn.blobFromImage(cv2.resize(img, (300, 300)), 1.0,(300, 300), (104.0, 177.0, 123.0))
    
    net.setInput(blob)
    detections = net.forward()
    for i in range(0, detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence < confThresh:
            continue

        box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
        (startX, startY, endX, endY) = box.astype("int")
        y = startY - 10 if startY - 10 > 10 else startY + 10
        cv2.rectangle(img, (startX, startY), (endX, endY),(0, 0, 255), 2)
        
    return img