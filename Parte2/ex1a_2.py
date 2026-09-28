#!/usr/bin/env python3

# imports
import cv2


# Main function
def main():
    print("SAVI exercise")

    # relative path
    image = cv2.imread("C:/Users/carolina marques/Desktop/SAVI/MySavi/images/dog_1.jpg")

    print("shape = " + str(image.shape))
    print("dtype = " + str(image.dtype))

    #cv2.imshow("Image", image)
    #cv2.waitKey(0)


    # Get the grayscale image
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    print("gray shape = " + str(gray_image.shape))
    print("gray dtype = " + str(gray_image.dtype))

    cv2.imshow("Gray Image", gray_image)
    cv2.waitKey(0)


if __name__ == "__main__":
    main()