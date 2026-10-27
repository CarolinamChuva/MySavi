
# ============================================================
# EXERCÍCIO 1 - BRILHO MÉDIO E CONTRASTE ALVO
# ============================================================
#
# Objetivo:
# - Ajustar uma imagem para atingir um brilho médio e um
#   contraste definidos pelo utilizador.
#
# - A imagem é alterada através da seguinte transformação:
#       I'(x,y) = s * I(x,y) + b
#
# - O parâmetro s controla o contraste da imagem.
# - O parâmetro b controla o brilho da imagem.
#
# Funcionamento do código:
# - Carrega a imagem original.
# - Define o brilho médio e o contraste pretendidos.
# - Calcula o brilho médio da imagem através da média dos pixels.
# - Calcula o contraste através do desvio padrão dos pixels.
# - Calcula o erro entre os valores atuais e os valores pretendidos.
# - Utiliza a função least_squares para encontrar os valores de
#   s e b que minimizam esses erros.
# - Aplica os valores encontrados à imagem.
# - Limita os valores dos pixels entre 0 e 255.
# - Mostra a imagem durante o processo de otimização e apresenta
#   o resultado final.
#
# O exercício é realizado em duas etapas:
# 1. Otimização usando apenas o erro do brilho médio.
# 2. Otimização usando simultaneamente o erro do brilho e
#    o erro do contraste.
#
# Objetivo final:
# - Obter uma imagem cujo brilho médio e contraste sejam o mais
#   próximos possível dos valores definidos como alvo.
# ============================================================

import json
import argparse
from pathlib import Path
from matplotlib import pyplot as plt
from line_class import Line
from scipy.optimize import least_squares
import cv2 as cv
import sys
import numpy as np
from functools import partial

def showFloatImage(window_name, image):
    image_uint8 = image.astype(np.uint8)
    cv.imshow(window_name,image_uint8)

def main():

    ap = argparse.ArgumentParser()
    ap.add_argument("-tab", "--target_average_brightness", type=int, required=False,
                        default=50,
                        help="")
    ap.add_argument("-tac", "--target_average_contrast", type=int, required=False,
                            default=50,
                            help="")

    args = vars(ap.parse_args())
    print("Input args: " + str(args))

    #Load images

    # Relative Path
    img_path = Path(__file__).parent.parent / 'images' / 'marvao_1.png'
    original_img = cv.imread(img_path)
    
    # Verifica se existe imagem
    if original_img is None:
        sys.exit("Could not read the image.")
    
    original_image_float = original_img.astype(float)


    # Create a data dictionary for storing all I need for the optimization
    data = {'original_image_float': original_image_float,
            'target_average_brightness': args['target_average_brightness'],
            'target_average_contrast': args['target_average_contrast'],
            'image_corrected': None}



    showFloatImage('Image', original_image_float)
    cv.waitKey(0)

    

    def objective_function(params, data):
        """The objective function is used to compute an error to inform the optimization procedure"""

        # Define os parametros numa lista: assume [m,b]
        s = params[0]
        b = params[1]
        print('s=' + str(s) + 'b=' + str(b))

        # Compute new image
        original_image = np.copy(data['original_image_float'])

        image_corrected = s * original_image + b
        image_corrected = np.minimum(image_corrected,255)
        image_corrected = np.maximum(image_corrected,0)

        # Compute the error
        average_color = np.average(image_corrected)

        error_brightness = data['target_average_brightness'] - average_color
        print('error_brightness: ' + str(error_brightness))


        std_color = np.std(image_corrected)
        error_contrast = data['target_average_contrast'] - std_color

        data['image_corrected'] = image_corrected

        # Visualization
        showFloatImage('image', image_corrected)
        key = cv.waitKey(200)

        if key == ord('q'):
            print('You pressed q, exiting.')
            exit(0)

        return [error_brightness, error_contrast]



    #----------------------------------------------------------
    # Execution
    #----------------------------------------------------------
   
    # Params will contain the s and b
    x0 = [1.0, 0.0] # initial parameters

    objective_function_with_fixed_data = partial(objective_function, data = data)
    result = least_squares(fun = objective_function_with_fixed_data, x0 = x0, verbose = 0, 
                           xtol = 1e-3, ftol=1e-3, gtol=1e-8)

    print('Result = '+str(result))

    showFloatImage('Final result', data['image_corrected'])
    key = cv.waitKey(0)


if __name__== "__main__":
    main()