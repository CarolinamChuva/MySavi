#!/usr/bin/env python3

# imports
import cv2
import numpy as np


# Main function
def main():
    print("SAVI exercise")

    # load image
    image = cv2.imread("C:/Users/carolina marques/Desktop/SAVI/MySavi/images/dog_1.jpg")

    height, width, channels = image.shape
    image = cv2.resize(image, (round(width/2), round(height/2)))

    cv2.imshow("Original", image)


    # --------------------------------
    # Segment green color to isolate the grass
    # --------------------------------

    # split BGR channels
    b, g, r = cv2.split(image)

    #cv2.imshow("Blue channel", b)
    #cv2.imshow("Green channel", g)
    #cv2.imshow("Red channel", r)

    #get mask by iposign limits on the channels
    mask_b = np.logical_and (b>0, b<100)

    print('mask_b dtype' + str(mask_b.dtype))
    image_to_show = mask_b.astype(np.uint8)*255
    #cv2.imshow('mask_b', image_to_show)

    #get mask by iposign limits on the channels
    mask_g = np.logical_and (g>130, g<255)

    print('mask_g dtype' + str(mask_g.dtype))
    image_to_show = mask_g.astype(np.uint8)*255
    #cv2.imshow('mask_g', image_to_show)

    #get mask by iposign limits on the channels
    mask_r = np.logical_and (r>0, r<100)
    
    print('mask_r dtype' + str(mask_r.dtype))
    image_to_show = mask_r.astype(np.uint8)*255
    #cv2.imshow('mask_r', image_to_show)

    mask= np.logical_and(mask_r, mask_b)
    mask= np.logical_and(mask, mask_g)
    cv2.imshow('mask', image_to_show)


    cv2.waitKey(0)


if __name__ == "__main__":
    main()