"""
Face Detection V1

Classifier Type :
    HarrCascade Frontal Face Classifier
    Haarcascade Eyes Classifier
    Haarcascade Smile Classifier

Output :
    Image with rectangle mark on face
    Total number of detected face
"""
import os
import cv2
from settings import ASSETS_DIR


face_path = os.path.join(ASSETS_DIR, "haarcascade_frontalface_default.xml")
eye_path = os.path.join(ASSETS_DIR, "haarcascade_eye.xml")
smile_path = os.path.join(ASSETS_DIR, "haarcascade_smile.xml")

face_cascade = cv2.CascadeClassifier(face_path)
eye_cascade = cv2.CascadeClassifier(eye_path)
smile_cascade = cv2.CascadeClassifier(smile_path)


def faceDetectionv1(img):
    img = cv2.imread(img)

    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    faces = face_cascade.detectMultiScale(gray, 1.4, 5)

    for face in faces:
        x, y, width, height = face
        # draw a rectangle for detection
        cv2.rectangle(
            img,
            (x, y),
            (x + width, y + height),
            (0, 0, 255),
            1,
        )
        roi_gray = gray[y : y + height, x : x + width]
        roi_color = img[y : y + height, x : x + width]
      
        smiles = smile_cascade.detectMultiScale(roi_gray)
        for (sx, sy, sw, sh) in smiles:
            cv2.rectangle(roi_color, (sx, sy), ((sx + sw), (sy + sh)), (0, 0, 255), 3)

        eyes = eye_cascade.detectMultiScale(roi_gray)
        for (ex, ey, ew, eh) in eyes:
            cv2.rectangle(
                roi_color,
                (ex, ey),
                (ex + ew, ey + eh),
                (0, 255, 0),
                2,
            )
    return img, len(faces)
