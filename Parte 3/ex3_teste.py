#!/usr/bin/env python3

# imports
import cv2
import numpy as np


# Main function
def main():

    print("SAVI exercise")


    # load image
    image = cv2.imread("C:/Users/carolina marques/Desktop/SAVI/MySavi/images/person_2.jpg")


    height, width, channels = image.shape

    # resize image
    image = cv2.resize(image, (round(width/2), round(height/2)))


    cv2.imshow("Original", image)



    # --------------------------------
    # Convert image to HSV
    # --------------------------------

    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)


    h, s, v = cv2.split(hsv)



    # --------------------------------
    # Get masks using HSV limits
    # --------------------------------


    # grass is green
    mask_h = np.logical_and(h > 30, h < 90)

    print("mask_h dtype = " + str(mask_h.dtype))


    mask_s = np.logical_and(s > 60, s < 255)

    print("mask_s dtype = " + str(mask_s.dtype))


    mask_v = np.logical_and(v > 40, v < 255)

    print("mask_v dtype = " + str(mask_v.dtype))



    # --------------------------------
    # Combine masks
    # --------------------------------

    mask_grass = np.logical_and(mask_h, mask_s)
    mask_grass = np.logical_and(mask_grass, mask_v)



    cv2.imshow(
        "grass mask",
        mask_grass.astype(np.uint8)*255
    )



    # --------------------------------
    # Remove noise
    # --------------------------------

    kernel = np.ones((5,5), np.uint8)


    mask_uint8 = mask_grass.astype(np.uint8)*255


    mask_clean = cv2.morphologyEx(
        mask_uint8,
        cv2.MORPH_OPEN,
        kernel,
        iterations=2
    )


    cv2.imshow("clean mask", mask_clean)



    # --------------------------------
    # Person mask
    # invert grass mask
    # --------------------------------


    mask_person = np.logical_not(mask_clean)


    mask_person = mask_person.astype(np.uint8)*255


    cv2.imshow("person mask", mask_person)



    # --------------------------------
    # Keep only the biggest component
    # --------------------------------


    numLabels, labels, stats, centroids = cv2.connectedComponentsWithStats(
        mask_person
    )


    print("numLabels = " + str(numLabels))


    largest_area = 0
    largest_index = 0



    for i in range(1, numLabels):

        area = stats[i, cv2.CC_STAT_AREA]


        if area > largest_area:

            largest_area = area
            largest_index = i



    print("largest area = " + str(largest_area))


    # create final mask
    final_mask = np.zeros_like(mask_person)


    final_mask[labels == largest_index] = 255



    cv2.imshow("Final person mask", final_mask)



    cv2.waitKey(0)



if __name__ == "__main__":
    main()