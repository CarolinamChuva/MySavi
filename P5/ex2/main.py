# -----------------------------------------------------------------------------
# SAVI - Parte 5, Exercício 2: Random Line Fitting
#
# Resumo do que foi feito:
# - Carrega os pontos (xs, ys) do points.json gerado no ex1 e desenha-os a preto.
# - Modelo de reta y = m*x + b (classe Line em line_class.py).
# - Em cada iteração sorteia m e b, redesenha a reta atual a azul e calcula o
#   erro face aos pontos (ground truth).
# - O erro usa o valor absoluto, sum|y - y'|, porque a soma com sinal
#   sum(y - y') permite que erros positivos e negativos se anulem.
# - Guarda a melhor reta (menor erro) e desenha-a a vermelho.
# - Termina ao pressionar uma tecla.

import argparse
from random import randint
import json
import random
import signal
import sys
from matplotlib import pyplot as plt

def signal_handler(sig, frame):
    print('You pressed Ctrl+C!')
    sys.exit(0)


def signal_handler_term(sig, frame):
    print('You pressed Ctrl+C!')
    sys.exit(0)


# Main function
def main(): # this is our main function
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler_term)
    print("SAVI exercise")

    # -------------------------------------------------------------------------
    # Initialization
    # -------------------------------------------------------------------------

    # initialize argparser
    ap = argparse.ArgumentParser()
    ap.add_argument("-ps", "--points_json", type=str, required=False, 
                    default="../ex1/points.json", help="Path to a json file containing the point coords", )
    
    args = ap.parse_args()
    args = vars(args) # transform the args into a dictionary
    print('Input args: ' + str(args))

    
    # Load json with points
    with open(args['points_json'], "r") as file:
        d = json.load(file)
        print('Read dict from file ' + args['points_json'] + ' with values:' + str(d))

    # Setup figure
    plt.title("Select points (press Q to abort)")
    plt.axis([-10, 10, -5, 5])
    plt.grid(True)

    plt.plot(d['xs'], d['ys'], 'ok')

    
    # -------------------------------------------------------------------------
    # Execution
    # -------------------------------------------------------------------------
    from MySavi.P5.ex2.line_class import Line

    line = Line() # Create instance
    best_line = Line() # Instance for best line
    lowest_error = 101023109238230 # a very large number 
    # TODO check for a better solution (Ghuilerme)

    while True:

        line.randomizeParams()
        line.draw(plt)

        # Compute error of the current line
        error = line.computeError(d['xs'], d['ys'])
        print('error = ' + str(round(error,3)))

        if error < lowest_error: # found a better line
            best_line.m = line.m
            best_line.b = line.b
            lowest_error = error


        best_line.draw(plt, color='r')


        plt.draw()
        pressed_key = plt.waitforbuttonpress(0.1)
        if pressed_key == True: # break cycle if key is pressed
            break




if __name__ == "__main__":
    main()




