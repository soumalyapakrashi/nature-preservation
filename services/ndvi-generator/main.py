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
    
    band_red_image_2017 = cv2.imread(band_red_path, cv2.IMREAD_GRAYSCALE)
    band_nir_image_2017 = cv2.imread(band_nir_path, cv2.IMREAD_GRAYSCALE)

    ndvi2017 = ndvi_generator.generateNDVI(band_red_image_2017, band_nir_image_2017)

    # Calculate some statistics for the images
    if(gpu_available == False):
        print(f"Min of NDVI 2017: {ndvi2017.mean()}")
        print(f"Max of NDVI 2017: {ndvi2017.max()}")
        print(f"Mean of NDVI 2017: {ndvi2017.mean()}")

    else:
        print(f"Min of NDVI 2017: {cp.min(ndvi2017)}")
        print(f"Max of NDVI 2017: {cp.max(ndvi2017)}")
        print(f"Mean of NDVI 2017: {cp.mean(ndvi2017)}")

        ndvi2017_cpu = cp.asnumpy(ndvi2017)
        del ndvi2017
        cp.get_default_memory_pool().free_all_blocks()

    # Get the NDVI image from 2022
    band_red_path = "D:/Programs/nature-preservation/storage/Siliguri/S2B_MSIL1C_20220213T043909_N0400_R033_T45RXK_20220213T064707.SAFE/GRANULE/L1C_T45RXK_A025799_20220213T044348/IMG_DATA/T45RXK_20220213T043909_B04.jp2"

    band_nir_path = "D:/Programs/nature-preservation/storage/Siliguri/S2B_MSIL1C_20220213T043909_N0400_R033_T45RXK_20220213T064707.SAFE/GRANULE/L1C_T45RXK_A025799_20220213T044348/IMG_DATA/T45RXK_20220213T043909_B08.jp2"

    band_red_image_2022 = cv2.imread(band_red_path, cv2.IMREAD_GRAYSCALE)
    band_nir_image_2022 = cv2.imread(band_nir_path, cv2.IMREAD_GRAYSCALE)

    ndvi2022 = ndvi_generator.generateNDVI(band_red_image_2022, band_nir_image_2022)

    # Calculate some statistics for the images
    if(gpu_available == False):
        print(f"Min of NDVI 2022: {ndvi2022.mean()}")
        print(f"Max of NDVI 2022: {ndvi2022.max()}")
        print(f"Mean of NDVI 2022: {ndvi2022.mean()}")

    else:
        print(f"\nMin of NDVI 2022: {cp.min(ndvi2022)}")
        print(f"Max of NDVI 2022: {cp.max(ndvi2022)}")
        print(f"Mean of NDVI 2022: {cp.mean(ndvi2022)}")

        ndvi2022_cpu = cp.asnumpy(ndvi2022)
        del ndvi2022
        cp.get_default_memory_pool().free_all_blocks()
    
    # Calculate the change in the two
    change_ndvi = ndvi2022_cpu - ndvi2017_cpu
