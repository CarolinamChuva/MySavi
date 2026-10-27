#!/usr/bin/env python3

# imports
import cv2
import numpy as np


# Main function
def main(): # this is our main function
    print("SAVI exercise")

    # relative path
    image = cv2.imread("C:/Users/carolina marques/Desktop/SAVI/MySavi/images/dog_1.jpg")
    height, width, channels = image.shape
    image = cv2.resize(image, (round(width/3), round(height/3)))

    cv2.imshow("Original", image)


    # --------------------------------
    # Darken the image
    # --------------------------------

    image_float = image.astype(float)
    # safe brighten the image
    altered_image = image_float - 50


    # some elements will have values over 255,
    # so we need to clip the values to 255
    altered_image = altered_image.clip(0, 255)


    # convert back to uint8
    altered_image = altered_image.astype(np.uint8)

    cv2.imshow("Altered Image", altered_image)


    cv2.waitKey(0)


if __name__ == "__main__":
    main()