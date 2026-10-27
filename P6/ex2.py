import argparse
from pathlib import Path
from scipy.optimize import least_squares
import cv2 as cv
import sys
import numpy as np
from functools import partial


# ----------------------------------------------------------
# Show image
# ----------------------------------------------------------

def showFloatImage(window_name, image):
    image_uint8 = image.astype(np.uint8)
    cv.imshow(window_name, image_uint8)


# ----------------------------------------------------------
# Main function
# ----------------------------------------------------------

def main():

    # ----------------------------------------------------------
    # Initialization
    # ----------------------------------------------------------

    print("SAVI - Exercise 2")

    # ----------------------------------------------------------
    # Load images
    # ----------------------------------------------------------

    # Relative paths
    train_path = Path(__file__).parent.parent / 'images' / 'machu_pichu1.png'
    query_path = Path(__file__).parent.parent / 'images' / 'query_warped.png'

    train_img = cv.imread(str(train_path))
    query_img = cv.imread(str(query_path))

    # Verify if images exist
    if train_img is None:
        sys.exit("Could not read the train image.")

    if query_img is None:
        sys.exit("Could not read the query image.")

    # Convert images to float
    train_image_float = train_img.astype(float)
    query_image_float = query_img.astype(float)

    # ----------------------------------------------------------
    # Create data dictionary
    # ----------------------------------------------------------

    data = {
        'train_image_float': train_image_float,
        'query_image_float': query_image_float,
        'train_corrected': None,
        'query_corrected': None
    }

    # ----------------------------------------------------------
    # Objective function
    # ----------------------------------------------------------

    def objective_function(params, data):
        """
        Objective function used by the optimization.

        Parameters:
            params = [s_train, b_train, s_query, b_query]

        Each image has its own scale (s) and bias (b).
        """

        # ------------------------------------------------------
        # Get parameters
        # ------------------------------------------------------

        s_train = params[0]
        b_train = params[1]

        s_query = params[2]
        b_query = params[3]

        print(
            "s_train =", s_train,
            "b_train =", b_train,
            "s_query =", s_query,
            "b_query =", b_query
        )

        # ------------------------------------------------------
        # Get original images
        # ------------------------------------------------------

        train_image = np.copy(data['train_image_float'])
        query_image = np.copy(data['query_image_float'])

        # ------------------------------------------------------
        # Correct both images
        # I'(x,y) = s * I(x,y) + b
        # ------------------------------------------------------

        train_corrected = s_train * train_image + b_train
        query_corrected = s_query * query_image + b_query

        # Keep pixel values between 0 and 255
        train_corrected = np.minimum(train_corrected, 255)
        train_corrected = np.maximum(train_corrected, 0)

        query_corrected = np.minimum(query_corrected, 255)
        query_corrected = np.maximum(query_corrected, 0)

        # Save corrected images
        data['train_corrected'] = train_corrected
        data['query_corrected'] = query_corrected

        # ------------------------------------------------------
        # Compute similarity error
        # ------------------------------------------------------

        # Difference between corresponding pixels
        error = train_corrected - query_corrected

        # ------------------------------------------------------
        # Visualization
        # ------------------------------------------------------

        showFloatImage('Train corrected', train_corrected)
        showFloatImage('Query corrected', query_corrected)

        key = cv.waitKey(200)

        if key == ord('q'):
            print('You pressed q, exiting.')
            sys.exit(0)

        # least_squares expects a vector of errors
        return error.flatten()

    # ----------------------------------------------------------
    # Execution
    # ----------------------------------------------------------

    # Initial parameters:
    #
    # train:
    #     s = 1
    #     b = 0
    #
    # query:
    #     s = 1
    #     b = 0
    #
    # Therefore:
    # [s_train, b_train, s_query, b_query]

    x0 = [1.0, 0.0, 1.0, 0.0]

    # Fix data argument
    objective_function_with_fixed_data = partial(
        objective_function,
        data=data
    )

    # ----------------------------------------------------------
    # Run optimization
    # ----------------------------------------------------------

    result = least_squares(
        fun=objective_function_with_fixed_data,
        x0=x0,
        verbose=1,
        xtol=1e-3,
        ftol=1e-3,
        gtol=1e-8
    )

    # ----------------------------------------------------------
    # Results
    # ----------------------------------------------------------

    print("Result = " + str(result))

    print("Optimized parameters:")
    print("s_train =", result.x[0])
    print("b_train =", result.x[1])
    print("s_query =", result.x[2])
    print("b_query =", result.x[3])

    # Show final images
    showFloatImage('Final train', data['train_corrected'])
    showFloatImage('Final query', data['query_corrected'])

    cv.waitKey(0)
    cv.destroyAllWindows()


# ----------------------------------------------------------
# Run main
# ----------------------------------------------------------

if __name__ == "__main__":
    main()