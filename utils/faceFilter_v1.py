import os
import numpy as np
import cv2

from settings import ASSETS_DIR


def apply_mask(face: np.array, mask: np.array):
    """Add the mask to the provided face, and return the face with mask."""
    mask_h, mask_w, _ = mask.shape
    face_h, face_w, _ = face.shape

    # Resize the mask to fit on face
    factor = min(face_h / mask_h, face_w / mask_w)
    new_mask_w = int(factor * mask_w)
    new_mask_h = int(factor * mask_h)
    new_mask_shape = (new_mask_w, new_mask_h)
    resized_mask = cv2.resize(mask, new_mask_shape)

    # Add mask to face - ensure mask is centered
    face_with_mask = face.copy()
    non_white_pixels = (resized_mask < 250).all(axis=2)
    off_h = int((face_h - new_mask_h) / 2)
    off_w = int((face_w - new_mask_w) / 2)
    face_with_mask[off_h : off_h + new_mask_h, off_w : off_w + new_mask_w][
        non_white_pixels
    ] = resized_mask[non_white_pixels]

    return face_with_mask


def faceFilterv1(input_image, mask_num):

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

    while True:
        # Capture frame-by-frame
        frame_h, frame_w, _ = input_image.shape
        # Convert to black-and-white
        gray = cv2.cvtColor(input_image, cv2.COLOR_RGB2GRAY)
        blackwhite = cv2.equalizeHist(gray)
        # Detect faces
        rects = cascade.detectMultiScale(
            blackwhite,
            scaleFactor=1.3,
            minNeighbors=4,
            minSize=(30, 30),
            flags=cv2.CASCADE_SCALE_IMAGE,
        )
        # Add mask to faces
        for x, y, w, h in rects:
            # crop a frame slightly larger than the face
            y0, y1 = int(y - 0.25 * h), int(y + 0.75 * h)
            x0, x1 = x, x + w
            # give up if the cropped frame would be out-of-bounds
            if x0 < 0 or y0 < 0 or x1 > frame_w or y1 > frame_h:
                continue
            input_image[y0:y1, x0:x1] = apply_mask(input_image[y0:y1, x0:x1], mask)
        return input_image
