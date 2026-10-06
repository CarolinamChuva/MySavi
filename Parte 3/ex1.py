#!/usr/bin/env python3 
# Shebang line" specifies the interpreter. 

# imports --------------------
import cv2
import numpy as np

def showMask(window_name, image):
    image_to_show = image.astype(np.uint8)*255
    cv2.imshow(window_name, image_to_show)

# Main function
def main(): # this is our main function
    print("SAVI exercise")

    cap =cv2.VideoCapture("C:/Users/carolina marques/Desktop/SAVI/MySavi/images/traffic.mp4")
    w =int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h =int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps=int(cap.get(cv2.CAP_PROP_FPS))
    print('fps ='+str(fps))

    #lê primeiro frame
    while True:
        ret,image_rgb = cap.read()
        if not ret:
            print("Processa o vídeo frame a frame")
            break
    
        cv2.imshow('Image', image_rgb)

        #-----------------------------------------------------------------
        #Como detetar os carros
        #------------------------------------------------------------------

        # quantos carros passarm pela faixa x?
        #que cores existem nos carros?
        
        key =cv2.waitKey(500)

        if key ==113:  #pressionar em Q para sair
            print("Sair")
            break 

if __name__ == "__main__":
    main()
