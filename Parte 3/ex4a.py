#!/usr/bin/env python3

# imports --------------------
import cv2
import numpy as np


def showMask(window_name, image):
    image_to_show = image.astype(np.uint8)*255
    cv2.imshow(window_name, image_to_show)


# Main function
def main():
    print("SAVI exercise")


    # relative path
    image = cv2.imread("C:/Users/carolina marques/Desktop/SAVI/MySavi/images/cenario.jpg")
    template = cv2.imread("C:/Users/carolina marques/Desktop/SAVI/MySavi/images/modelo.png")


    HEIGHT, WIDTH, NC = image.shape
    height, width, num_channels = template.shape

    template=cv2.resize(template, (round(height/2), round(width/2)))

    cv2.imshow('Image', image)
    cv2.imshow('Template', template)


    # --------------------------------
    # Template matching for detection
    # --------------------------------
    res = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)
    res_uint8 = (res*255).astype(np.uint8)
    #cv2.imshow('Matching Result', res_uint8)

    # Find maximum value of correlation and its coordinates
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    print("max_loc = ", str(max_loc))

    # Extract bounding box coordinates
    x = max_loc[0]
    y = max_loc[1]
    w = width
    h = height

    # Draw rectangle around detected object
    image_annotated = image.copy()
    cv2.rectangle(image_annotated,
                  (x, y),
                  (x+w, y+h),
                  (255, 0, 0),
                  2)

    cv2.imshow('Image Annotated', image_annotated)
    cv2.waitKey(0)


if __name__ == "__main__":
    main()