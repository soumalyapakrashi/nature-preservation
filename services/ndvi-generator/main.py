import matplotlib.pyplot as plt
import numpy as np
import cupy as cp
import cv2
import GPUtil

import ndvi_generator
import visualizations

# Check whether GPU is available and set flag accordingly
available_gpu_list = GPUtil.getAvailable()

if(len(available_gpu_list) == 0):
    gpu_available: bool = False
else:
    gpu_available: bool = True


# This class stores objects to the disk.
# This decreases the execution time of the program as intermediate calculations
# can be saved to the disk and does not need to be recalculated at each run.
class TempObjectStorage:
    @staticmethod
    def storeMatrix(matrix: np.ndarray, filename: str) -> None:
        np.save(file = filename, arr = matrix)
    
    @staticmethod
    def loadMatrix(filename: str) -> np.ndarray:
        loaded_matrix: np.ndarray = np.load(file = filename)
        return loaded_matrix


if(__name__ == "__main__"):
    # Get the NDVI image from Sentinel 2017
    band_red_path = "D:/Programs/nature-preservation/storage/Siliguri/S2A_MSIL1C_20170115T044121_N0204_R033_T45RXK_20170115T044124.SAFE/GRANULE/L1C_T45RXK_A008181_20170115T044124/IMG_DATA/T45RXK_20170115T044121_B04.jp2"

    band_nir_path = "D:/Programs/nature-preservation/storage/Siliguri/S2A_MSIL1C_20170115T044121_N0204_R033_T45RXK_20170115T044124.SAFE/GRANULE/L1C_T45RXK_A008181_20170115T044124/IMG_DATA/T45RXK_20170115T044121_B08.jp2"
    
    band_red_image = cv2.imread(band_red_path, cv2.IMREAD_GRAYSCALE)
    band_nir_image = cv2.imread(band_nir_path, cv2.IMREAD_GRAYSCALE)

    ndvi = ndvi_generator.generateNDVI(band_red_image, band_nir_image)
