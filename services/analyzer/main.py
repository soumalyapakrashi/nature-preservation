import numpy as np
import os

import generate_stats

if(__name__ == "__main__"):
    ndvi_matrix_path = ""

    # Load the NDVI matrix
    ndvi: np.ndarray = np.load(file = os.path.join(ndvi_matrix_path, "ndvi_matrix.npy"))
