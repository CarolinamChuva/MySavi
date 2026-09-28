#!/usr/bin/env python3

# imports
import cv2
import numpy as np


def safe_alter_image(image, value, curtain_position):

    # convert image to float to avoid overflow
    image_float = image.astype(float)

    height, width, nc = image.shape

    # copy original image
    altered_image = image_float.copy()


    # darken only the part covered by the curtain
    altered_image[:, :curtain_position, :] = (
        image_float[:, :curtain_position, :] + value
    )


    # keep values between 0 and 255
    altered_image = altered_image.clip(0, 255)


    # convert back to uint8
    altered_image = altered_image.astype(np.uint8)


    return altered_image



# Main function
def main():

    print("SAVI exercise")


    # load image
    image = cv2.imread("C:/Users/carolina marques/Desktop/SAVI/MySavi/images/dog_1.jpg")

    height, width, channels = image.shape

    # resize image
    image = cv2.resize(
        image,
        (round(width/3), round(height/3))
    )

    cv2.imshow("Original", image)

    # update dimensions after resize
    height, width, channels = image.shape

    # --------------------------------
    # Curtain effect + progressive darkening
    # --------------------------------

    for i in range(0, width + 1, 20):

        # darkness increases with time
        darkness = -(i // 20) * 10

        # apply curtain and darkening
        altered_image = safe_alter_image(
            image,
            darkness,
            i
        )

        cv2.imshow("Curtain effect", altered_image)

        # animation speed
        cv2.waitKey(100)


    cv2.waitKey(0)

if __name__ == "__main__":
    main()