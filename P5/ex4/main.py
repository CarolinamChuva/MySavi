# -----------------------------------------------------------------------------
# SAVI - Parte 5, Exercício 4: Composed model fitting
#
# Resumo do que foi feito:
# - Carrega os pontos do points.json (ex1) e desenha-os a preto.
# - Modelo composto (classe ComposedModel): reta y = m*x + b para x <= 0 e
#   parábola y = s*(x - dx)^2 + dy para x > 0, com parâmetros [m, b, s, dx, dy].
# - Fase 1 (aleatória): sorteia os parâmetros N vezes, desenha o modelo a azul
#   e guarda os melhores (menor erro sum|y - y'|), desenhados a vermelho.
# - Fase 2 (least squares): scipy.optimize.least_squares parte dos melhores
#   parâmetros da fase 1, minimizando o vetor de resíduos (y - y').
# - Resultado final desenhado a verde. Uma tecla interrompe a fase atual.
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

    from MySavi.P5.ex4.line_class import Line
    from MySavi.P5.ex4.parabola_class import Parabola
    parabola = Parabola() # Create instance
    parabola.randomizeParams() # Randomize parameters

    def objective_function(params):
        """ The objective function is used to compute an error to inform the optimization procedure
        """

        # Define the parameters in a list: assume  [m, b]
        parabola.s = params[0]
        parabola.dx = params[1]    
        parabola.dy = params[2]    

        error = parabola.computeError(d['xs'], d['ys'])
        print('Error = ' + str(error))
        
        parabola.draw(plt)

        plt.draw()
        pressed_key = plt.waitforbuttonpress(0.1)
        if pressed_key == True: # break cycle if key is pressed
            exit(0) # to terminate the optimizations procedure


        return error
    
    # -------------------------------------------------------------------------
    # Execution
    # -------------------------------------------------------------------------

    x0 = [parabola.s, parabola.dx, parabola.dy] # initial guess for the parameters

    result = least_squares(fun=objective_function, x0=x0, verbose=0, xtol=1e-33)


    print('Result = ' + str(result))


    plt.show()

if __name__ == "__main__":
    main()




