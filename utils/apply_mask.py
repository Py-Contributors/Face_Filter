import numpy as np
import cv2


def applyMask(face: np.array, mask: int):
    """Add the mask to the provided face, and return the face with mask.

    args:
        face (np.array): Face image
        mask (int): Mask number to apply

    returns:
        face (np.array): Face image with mask applied

    """
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
    face_with_mask[off_h: off_h + new_mask_h, off_w: off_w + new_mask_w][
        non_white_pixels
    ] = resized_mask[non_white_pixels]

    return face_with_mask
