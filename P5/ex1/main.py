# -----------------------------------------------------------------------------
# SAVI - Parte 5, Exercício 1: generate_data
#
# Resumo do que foi feito:
# - Figura matplotlib com um sistema cartesiano x∈[-10,10] e y∈[-5,5] e grelha.
# - Cada clique do rato dentro dos eixos adiciona um ponto (arredondado a 3
#   casas decimais), desenhado como 'x' vermelho. Cliques fora dos eixos são
#   ignorados (event.inaxes).
# - Usa callbacks de eventos (button_press_event e key_press_event) em vez de
#   um ciclo com ginput, e plt.show() bloqueia até a janela fechar.
# - A tecla ESC fecha a figura e termina a recolha de pontos.
# - No fim, os pontos são gravados num dicionário
#   {'xs': [x0,...,xn], 'ys': [y0,...,yn]} em points.json (argumento -f).
# -----------------------------------------------------------------------------

import argparse
from random import randint
import json
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
    # ap.add_argument("-is", "--image_scale", type=float, required=False, 
                    # default=1.0, help="Scale of images to display", )
    
    args = ap.parse_args()
    args = vars(args) # transform the args into a dictionary
    print('Input args: ' + str(args))


    plt.rcParams['keymap.quit'] = []  # stop matplotlib closing the window on 'q'

    fig = plt.figure()
    plt.title("Select points (press Q to abort)")
    plt.axis([-10, 10, -5, 5])
    plt.grid(True)

    state = {'abort': False}

    def on_key(event):
        if event.key in ('q', 'Q'):
            print('You pressed Q, aborting loop')
            state['abort'] = True

    fig.canvas.mpl_connect('key_press_event', on_key)

    d = {'xs': [], 'ys': []}
    while True:

        click = plt.ginput(1)  # returns on mouse click or key press
        if state['abort'] or not click:  # Q pressed, or window closed
            break
        print('click=' + str(click))

        x = round(float(click[0][0]),3)
        y = round(float(click[0][1]),3)

        d['xs'].append(x)
        d['ys'].append(y)

        plt.plot(d['xs'], d['ys'], 'xr')

        print('d='+ str(d))

        plt.draw()
        plt.waitforbuttonpress(0.1)



    print('for loop finished')
    # Save the dict to a json
    filename = 'points.json'
    with open(filename,'w') as fp:
        json.dump(d, fp, sort_keys=True, indent=4)
        print('Points saved to ' + filename)



    # -------------------------------------------------------------------------
    # Execution
    # -------------------------------------------------------------------------



    


if __name__ == "__main__":
    main()




