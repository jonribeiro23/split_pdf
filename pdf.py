import os
import re
import argparse
import pytesseract
from pytesseract import Output
import cv2
import numpy as np
import fitz
from io import BytesIO
from PIL import Image
import pandas as pd
import filetype

# Path Of The Tesseract OCR engine
TESSERACT_PATH = "C:\Program Files\Tesseract-OCR\tesseract.exe"
# Include tesseract executable
pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH


def pix2np(pix):
    """
    Converts a pixmap buffer into a numpy array
    """
    # pix.samples = sequence of bytes of the image pixels like RGBA
    #pix.h = height in pixels
    #pix.w = width in pixels
    # pix.n = number of components per pixel (depends on the colorspace and alpha)
    im = np.frombuffer(pix.samples, dtype=np.uint8).reshape(
        pix.h, pix.w, pix.n)
    try:
        im = np.ascontiguousarray(im[..., [2, 1, 0]])  # RGB To BGR
    except IndexError:
        # Convert Gray to RGB
        im = cv2.cvtColor(im, cv2.COLOR_GRAY2RGB)
        im = np.ascontiguousarray(im[..., [2, 1, 0]])  # RGB To BGR
    return im

# Image Pre-Processing Functions to improve output accurracy
# Convert to grayscale
def grayscale(img):
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Remove noise
def remove_noise(img):
    return cv2.medianBlur(img, 5)

# Thresholding
def threshold(img):
    # return cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    return cv2.threshold(img, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

# dilation
def dilate(img):
    kernel = np.ones((5, 5), np.uint8)
    return cv2.dilate(img, kernel, iterations=1)

# erosion
def erode(img):
    kernel = np.ones((5, 5), np.uint8)
    return cv2.erode(img, kernel, iterations=1)

# opening -- erosion followed by a dilation
def opening(img):
    kernel = np.ones((5, 5), np.uint8)
    return cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)

# canny edge detection
def canny(img):
    return cv2.Canny(img, 100, 200)

# skew correction
def deskew(img):
    coords = np.column_stack(np.where(img > 0))
    angle = cv2.minAreaRect(coords)[-1]
    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle
    (h, w) = img.shape[:2]
    center = (w//2, h//2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(
        img, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    return rotated

# template matching
def match_template(img, template):
    return cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)

def convert_img2bin(img):
    """
    Pre-processes the image and generates a binary output
    """
    # Convert the image into a grayscale image
    output_img = grayscale(img)
    # Invert the grayscale image by flipping pixel values.
    # All pixels that are grater than 0 are set to 0 and all pixels that are = to 0 are set to 255
    output_img = cv2.bitwise_not(output_img)
    # Converting image to binary by Thresholding in order to show a clear separation between white and blacl pixels.
    output_img = threshold(output_img)
    return output_img

def display_img(title, img):
    """Displays an image on screen and maintains the output until the user presses a key"""
    cv2.namedWindow('img', cv2.WINDOW_NORMAL)
    cv2.setWindowTitle('img', title)
    cv2.resizeWindow('img', 1200, 900)
    # Display Image on screen
    cv2.imshow('img', img)
    # Mantain output until user presses a key
    cv2.waitKey(0)
    # Destroy windows when user presses a key
    cv2.destroyAllWindows()