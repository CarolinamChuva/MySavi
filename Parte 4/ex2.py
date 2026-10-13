#!/usr/bin/env python3 
# Shebang line" specifies the interpreter. 

# imports --------------------
import argparse
import cv2
import json
import numpy as np
import signal
import sys
from colorama import Fore, Style

def signal_handler(sig, frame):
    print('You pressed Ctrl+C!')
    sys.exit(0)


def signal_handler_term(sig, frame):
    print('You pressed Ctrl+C!')
    sys.exit(0)


def showMask(window_name, image):
    image_to_show = image.astype(np.uint8)*255
    cv2.imshow(window_name, image_to_show)

#def showScaledImage(window_name, image, scale):


# Main function
def main(): # this is our main function
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler_term)
    print("SAVI exercise")

    # -------------------------------------------------------------------------
    # Initialization
    # -------------------------------------------------------------------------

    # initialize argparser
    ap = argparse.ArgumentParser()
    ap.add_argument("-lbf", "--lane_bboxes_filename", type=str, required=False, 
                    default='lane_bboxes.json',
                    help="Name of the json file containing the lane bounding boxes.", )
    ap.add_argument("-acr", "--average_color_reference", type=int, required=False, 
                    default=125,
                    help="Average reference color of the road")

    ap.add_argument("-dt", "--detection_threshold", type=int, required=False, 
                    default=40,
                    help="Detection threshold for deciding when a significant change occured.")

    args = ap.parse_args()
    args = vars(args) # transform the args into a dictionary
    print('Input args: ' + str(args))

    train_image = cv2.imread('C:/Users/carolina marques/OneDrive - Universidade de Aveiro/Desktop/SAVI/MySavi/images/1.png')
    query_image = cv2.imread('C:/Users/carolina marques/OneDrive - Universidade de Aveiro/Desktop/SAVI/MySavi/images/2.png')

    # -------------------------------------------------------------------------
    # Initialization
    # -------------------------------------------------------------------------

    cv2.namedWindow('Train',cv2.WINDOW_Normal)
    cv2.imshow('Train',train_image)
    cv2.imshow('Query',query_image)

if __name__ == "__main__":
    main()