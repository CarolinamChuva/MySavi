#!/usr/bin/env python3 

# imports --------------------
import cv2
import numpy as np


# variáveis globais para o rato
drawing = False
ix, iy = -1, -1
fx, fy = -1, -1
image_copy = None


# função para desenhar o retângulo
def draw_rectangle(event, x, y, flags, param):

    global drawing, ix, iy, fx, fy, image_copy

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix, iy = x, y

    elif event == cv2.EVENT_MOUSEMOVE:

        if drawing:
            image_copy = image.copy()

            cv2.rectangle(image_copy,
                          (ix, iy),
                          (x, y),
                          (255, 0, 0),
                          2)

            cv2.imshow("Image", image_copy)

    elif event == cv2.EVENT_LBUTTONUP:

        drawing = False
        fx, fy = x, y

        cv2.rectangle(image_copy,
                      (ix, iy),
                      (fx, fy),
                      (255, 0, 0),
                      2)

        cv2.imshow("Image", image_copy)


# Main function
def main():

    global image, image2, image_copy


    print("SAVI exercise")


    # carregar imagem
    image = cv2.imread("C:/Users/carolina marques/Desktop/SAVI/MySavi/images/husky_for_extracting_template.png")
    image2 = cv2.imread("C:/Users/carolina marques/Desktop/SAVI/MySavi/images/cenario_2.jpg")
    image_copy = image.copy()


    # mostrar imagem para selecionar
    cv2.namedWindow("Image")
    cv2.setMouseCallback("Image", draw_rectangle)


    cv2.imshow("Image", image)
    cv2.imshow("Image2", image2)


    print("Seleciona o objeto com o rato e carrega numa tecla")


    cv2.waitKey(0)


    # --------------------------------
    # Criar template a partir da seleção
    # --------------------------------


    # garantir que o retângulo foi feito da esquerda para direita
    x1 = min(ix, fx)
    y1 = min(iy, fy)

    x2 = max(ix, fx)
    y2 = max(iy, fy)


    # cortar o objeto escolhido
    template = image[y1:y2, x1:x2]


    cv2.imshow("Template escolhido", template)



    HEIGHT, WIDTH, NC = image.shape
    height, width, num_channels = template.shape

    # --------------------------------
    # Template matching for detection
    # --------------------------------


    res = cv2.matchTemplate(image2,template,cv2.TM_CCOEFF_NORMED)
    res_uint8 = (res*255).astype(np.uint8)

    #cv2.imshow("Matching Result",res_uint8)

    # encontrar melhor correspondência
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

    print("max_loc = ", str(max_loc))
    print("score = ", str(max_val))


    # coordenadas do retângulo encontrado
    x = max_loc[0]
    y = max_loc[1]
    w = width
    h = height

    # desenhar resultado

    image_annotated = image2.copy()
    cv2.rectangle(image_annotated,(x,y),(x+w,y+h),(255,0,0),2)

    cv2.imshow("Image Annotated",image_annotated)

    cv2.waitKey(0)



if __name__ == "__main__":
    main()