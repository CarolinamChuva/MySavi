#!/usr/bin/env python3

# imports
import cv2                                                                                  #Biblio para processamento de imagens
import numpy as np                                                                          #Biblio para arrays e operações matemáticas


# Main function
def main():
    print("SAVI exercise")                                                                  #Escreve isto no terminal

    # relative path
    image = cv2.imread("C:/Users/carolina marques/Desktop/SAVI/MySavi/images/dog_1.jpg")   #Lê a imagem do disco e guarda-a numa variável chamada image
 
    print("shape = " + str(image.shape))                                                   # Mostra as dimensões da imagem (altura, largura, canais)
    print("dtype = " + str(image.dtype))                                                   # Mostra o tipo de dados dos pixels da imagem (normalmente uint8)


    cv2.imshow("Imagem Original", image)
    cv2.waitKey(0)


    # Get the grayscale image
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    print("gray shape = " + str(gray_image.shape))
    print("gray dtype = " + str(gray_image.dtype))

    #cv2.imshow("Gray Image", gray_image)
    #cv2.waitKey(0)


    # How to get a portion of the image?

    left_side_image = gray_image[:, :512]

    #cv2.imshow("Left side image", left_side_image)


    dog_tail = gray_image[1:round(895/2), 512:1024]

    #cv2.imshow("Dog Tail", dog_tail)


    # resize an image

    resize_image = cv2.resize(gray_image, (256, 256))

    #cv2.imshow("Resized Image", resize_image)


    # brighten the image

    bright_image = gray_image + 20

    #cv2.imshow("Bright Image", bright_image)
    #cv2.waitKey(0)

    #
    # Challenge to solve overflow
    #

    print("gray dtype = " + str(gray_image.dtype))

    image_float = gray_image.astype(float)

    print("image_float dtype = " + str(image_float.dtype))


    # safe brighten the image
    image_brightened = image_float + 20


    # some elements will have values over 255,
    # so we need to clip the values to 255
    image_brightened = image_brightened.clip(0, 255)


    # convert back to uint8
    image_brightened = image_brightened.astype(np.uint8)

if __name__ == "__main__":
    main()