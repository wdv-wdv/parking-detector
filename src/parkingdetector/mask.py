import cv2
import numpy as np
import os.path
import sys
from config import Config

def apply(img):
    print("Apply mask")
    
    maskFilename =  Config().GetMaskFilename() #  "/home/python-env/parking/mask.jpg" 
    if (not os.path.isfile(maskFilename)):
        print("mask file not found")
        sys.exit(1)

    masking = cv2.imread(maskFilename)

    mask = cv2.inRange(masking, np.array([255,255,255]), np.array([255,255,255]))
    img = cv2.bitwise_and(img,img, mask= mask)

    masking = cv2.cvtColor(masking, cv2.COLOR_BGR2GRAY)

    contours, hierarchy = cv2.findContours(image=masking, mode=cv2.RETR_LIST, method=cv2.CHAIN_APPROX_NONE)

    return img, contours