import cv2
import numpy as np


def detect_bin_status(image_path):
    """
    Analyze the image and determine bin status (Full/Empty/Partially Full).
    """
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if image is None:
        raise ValueError("Image not found or invalid format.")

    # Perform some image processing (e.g., thresholding)
    thresholded = cv2.threshold(image, 128, 255, cv2.THRESH_BINARY)
    white_pixels = cv2.countNonZero(thresholded)
    total_pixels = thresholded.size
    fill_percentage = (white_pixels / total_pixels) * 100

    # Determine bin status based on fill percentage
    if fill_percentage > 80:
        return 'Full'
    elif 20 <= fill_percentage <= 60:
        return 'Partially Full'
    else:
        return 'Empty'

