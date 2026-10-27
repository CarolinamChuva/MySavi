#!/usr/bin/env python3

# imports
import cv2
import numpy as np


def safe_alter_image(image, value):

    # alter only the left side

    image_float = image.astype(float)

    height, width, nc = image.shape

    # safe alter the image
    altered_image = image_float.copy()

    # change only the left side
    altered_image[:, :round(width/2), :] = image_float[:, :round(width/2), :] + value

    # some elements will have values over 255,
    # so we need to clip the values to 255

    altered_image = altered_image.clip(0, 255)

    # convert back to uint8

    altered_image = altered_image.astype(np.uint8)

    return altered_image



# Main function
def main():

    print("SAVI exercise")

    # relative path
    image = cv2.imread("C:/Users/carolina marques/Desktop/SAVI/MySavi/images/dog_1.jpg")

    height, width, channels = image.shape

    # resize image
    image = cv2.resize(image, (round(width/3), round(height/3)))

    cv2.imshow("Original", image)


    # --------------------------------
    # Darken the image
    # --------------------------------

    altered_image = safe_alter_image(image, -50)

    cv2.imshow("Altered Image", altered_image)


    # --------------------------------
    # Create a sequence of progressive darkening
    # of the left side of the image
    # --------------------------------

    for i in range(0, 20):

        value_i = -i * 10

        altered_image = safe_alter_image(image, value_i)

        cv2.imshow("Altered Image", altered_image)

        cv2.waitKey(500)


    cv2.waitKey(0)


if __name__ == "__main__":
    main()