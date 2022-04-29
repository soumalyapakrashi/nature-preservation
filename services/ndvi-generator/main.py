import matplotlib.pyplot as plt
import numpy as np
import cv2

import ndvi_generator
import visualizations


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
    band_red_path = "C:/Users/User/Downloads/L1C_T43REL_A008396_20170130T053159/S2A_MSIL1C_20170130T053041_N0204_R105_T43REL_20170130T053159.SAFE/GRANULE/L1C_T43REL_A008396_20170130T053159/IMG_DATA/T43REL_20170130T053041_B04.jp2"

    band_nir_path = "C:/Users/User/Downloads/L1C_T43REL_A008396_20170130T053159/S2A_MSIL1C_20170130T053041_N0204_R105_T43REL_20170130T053159.SAFE/GRANULE/L1C_T43REL_A008396_20170130T053159/IMG_DATA/T43REL_20170130T053041_B08.jp2"
    
    band_red_image_2017 = cv2.imread(band_red_path, cv2.IMREAD_GRAYSCALE)
    band_nir_image_2017 = cv2.imread(band_nir_path, cv2.IMREAD_GRAYSCALE)

    ndvi2017 = ndvi_generator.generateNDVI(band_red_image_2017, band_nir_image_2017)

    # Get the NDVI image from 2020
    band_red_path = "C:/Users/User/Downloads/L1C_T43REL_A015146_20200130T053806/S2B_MSIL1C_20200130T053049_N0208_R105_T43REL_20200130T090639.SAFE/GRANULE/L1C_T43REL_A015146_20200130T053806/IMG_DATA/T43REL_20200130T053049_B04.jp2"

    band_nir_path = "C:/Users/User/Downloads/L1C_T43REL_A015146_20200130T053806/S2B_MSIL1C_20200130T053049_N0208_R105_T43REL_20200130T090639.SAFE/GRANULE/L1C_T43REL_A015146_20200130T053806/IMG_DATA/T43REL_20200130T053049_B08.jp2"

    band_red_image_2020 = cv2.imread(band_red_path, cv2.IMREAD_GRAYSCALE)
    band_nir_image_2020 = cv2.imread(band_nir_path, cv2.IMREAD_GRAYSCALE)

    ndvi2020 = ndvi_generator.generateNDVI(band_red_image_2020, band_nir_image_2020)

    # Calculate the amount of healthy vegetation.
    # Healthy vegetation is considered to be those whose NDVI is more than 0.5
    healthy2017 = 0
    healthy2020 = 0
    for row in range(ndvi2017.shape[0]):
        for column in range(ndvi2017.shape[1]):
            if(ndvi2017[row][column] >= 0.5):
                healthy2017 += 1
            
            if(ndvi2020[row][column] >= 0.5):
                healthy2020 += 1

    # Calculate the change in the two
    change_ndvi = ndvi2020 - ndvi2017

    # Calculate the change in forest cover (NDVI)
    total_pixels = change_ndvi.shape[0] * change_ndvi.shape[1]
    no_change_pixels = 0
    positive_change_pixels = 0
    negative_change_pixels = 0

    # Iterate over all the pixels and figure out where changes have been observed in NDVI
    for row in range(change_ndvi.shape[0]):
        for column in range(change_ndvi.shape[1]):
            if(change_ndvi[row][column] == 0):
                no_change_pixels += 1
            elif(change_ndvi[row][column] > 0):
                positive_change_pixels += 1
            else:
                negative_change_pixels += 1

    # Print the details calculated above
    print(f"No Change Pixels = {(no_change_pixels / total_pixels) * 100.0}%")
    print(f"Positive Change Pixels = {(positive_change_pixels / total_pixels) * 100.0}%")
    print(f"Negative Change Pixels = {(negative_change_pixels / total_pixels) * 100.0}%")

    print(f"Healthy Vegetation in 2017 = {(healthy2017 / total_pixels) * 100.0}%")
    print(f"Healthy Vegetation in 2020 = {(healthy2020 / total_pixels) * 100.0}%")
    print(f"Change in Vegetation = {((healthy2020 - healthy2017) / total_pixels) * 100.0}%")
