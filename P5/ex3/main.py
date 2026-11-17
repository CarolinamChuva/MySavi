# -----------------------------------------------------------------------------
# SAVI - Parte 5, Exercício 3: Line fitting com scipy.optimize.least_squares
#
# Resumo do que foi feito:
# - Carrega os pontos do points.json (ex1) e desenha-os a preto.
# - Substitui a geração aleatória de m e b do ex2 pela função least_squares
#   do scipy, partindo de uma estimativa inicial aleatória.
# - A função objetivo devolve o vetor de resíduos (y - y') de cada ponto, e o
#   least_squares minimiza a soma dos seus quadrados.
# - Em cada chamada da função objetivo a reta é redesenhada a azul, e o
#   erro é impresso. Carregar numa tecla interrompe a otimização.
# - No fim imprime o resultado e mostra a reta final a vermelho.
# -----------------------------------------------------------------------------

import argparse
from random import randint
import json
import random
import signal
import sys
from matplotlib import pyplot as plt
from scipy.optimize import least_squares

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

    from MySavi.P5.ex3.line_class import Line
    line = Line() # Create instance
    line.randomizeParams() # Randomize parameters

    def objective_function(params):
        """ The objective function is used to compute an error to inform the optimization procedure
        """

        # Define the parameters in a list: assume  [m, b]
        line.m = params[0]
        line.b = params[1]    

        error = line.computeError(d['xs'], d['ys'])
        print('Error = ' + str(error))
        print('m = ' + str(line.m))
        print('b = ' + str(line.b))
        
        line.draw(plt)

        plt.draw()
        pressed_key = plt.waitforbuttonpress(0.1)
        if pressed_key == True: # break cycle if key is pressed
            exit(0) # to terminate the optimizations procedure


        return error
    
    # -------------------------------------------------------------------------
    # Execution
    # -------------------------------------------------------------------------

    x0 = [line.m, line.b] # initial guess for the parameters

    result = least_squares(fun=objective_function, x0=x0, verbose=0, xtol=1e-33)


    print('Result = ' + str(result))

if __name__ == "__main__":
    main()




