import matplotlib.pyplot as plt
import numpy as np
import cupy as cp
import cv2
import GPUtil
from dotenv import load_dotenv
import os
import mariadb

import ndvi_generator
import visualizations

load_dotenv()

# Check whether GPU is available and set flag accordingly
available_gpu_list = GPUtil.getAvailable()

if(len(available_gpu_list) == 0):
    gpu_available: bool = False
else:
    gpu_available: bool = True


# This class stores objects to the disk.
# This decreases the execution time of the program as intermediate calculations
# can be saved to the disk and does not need to be recalculated at each run.
class ObjectStorage:
    @staticmethod
    def storeMatrix(matrix: np.ndarray, path: str, filename: str) -> None:
        os.makedirs(path, exist_ok = True)
        np.save(file = os.path.join(path, filename), arr = matrix, allow_pickle = False)
    
    @staticmethod
    def loadMatrix(filename: str) -> np.ndarray:
        loaded_matrix: np.ndarray = np.load(file = filename)
        return loaded_matrix


if(__name__ == "__main__"):
<<<<<<< HEAD
    # Connect to database
    try:
        connection = mariadb.connect(
            user = os.environ.get("MYSQL_USER"),
            password = os.environ.get("MYSQL_PASSWORD"),
            host = os.environ.get("MYSQL_HOST"),
            port = int(os.environ.get("MYSQL_PORT")),
            database = os.environ.get("MYSQL_DATABASE")
        )
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        exit(1)
    
    # Get the cursor to the database
    cursor = connection.cursor()
    
    # Get the images which have not been processed
    cursor.execute("SELECT id, area_id, year, sat_data_path FROM STORED_DATA_INFO WHERE ndvi_generated = ?", (0,))

    # This will contain the information about every image calculated so that database can be updated accordingly
    database_update = []

    # Iterate over each tuple
    for (id, area_id, year, sat_data_path) in cursor:
        # List all the image files in the required directory
        image_files = os.listdir(sat_data_path)

        # Iterate over all the image files and choose only bands 4 and 8.
        # Load the chosen images using OpenCV.
        for image_file in image_files:
            if(image_file.endswith("B04.jp2")):
                band_red_image = cv2.imread(os.path.join(sat_data_path, image_file), cv2.IMREAD_GRAYSCALE)

            elif(image_file.endswith("B08.jp2")):
                band_nir_image = cv2.imread(os.path.join(sat_data_path, image_file), cv2.IMREAD_GRAYSCALE)

        # Generate the NDVI matrix.
        # This ndvi variable will be a np.ndarray if no GPU is available.
        # But if GPU is available, then it will be cp.ndarray.
        ndvi = ndvi_generator.generateNDVI(band_red_image, band_nir_image)

        # If executing on GPU, bring the matrix to CPU memory and free GPU memory
        if(gpu_available == True):
            ndvi = cp.asnumpy(ndvi)
            cp.get_default_memory_pool().free_all_blocks()
        
        # Store the NDVI matrix to object storage
        save_path = os.path.join(
            os.environ.get("NDVI_STORAGE_BASE_DIR"),
            str(area_id),
            str(year)
        )

        # Store the matrix to object storage
        ObjectStorage.storeMatrix(ndvi, save_path, "ndvi_matrix.npy")

        database_update.append((id, save_path))

    # Update the database to reflect that images have been processed
    for (id, save_path) in database_update:
        # Update database indicating that NDVI images have been calculated
        cursor.execute("UPDATE STORED_DATA_INFO SET ndvi_generated = ? WHERE id = ?", (1, id))

        # Update database indicating where the NDVI files have been stored
        cursor.execute(
            "UPDATE STORED_DATA_INFO SET ndvi_data_path = ? WHERE id = ?",
            (save_path, id)
        )
    
    # Commit the changes to the database
    connection.commit()

    # Close the connection to the database
    connection.close()
=======
    # Get the NDVI image from Sentinel 2017
    band_red_path = "C:/Users/debal/Downloads/L1C_T43REL_A008396_20170130T053159/S2A_MSIL1C_20170130T053041_N0204_R105_T43REL_20170130T053159.SAFE/GRANULE/L1C_T43REL_A008396_20170130T053159/IMG_DATA/T43REL_20170130T053041_B04.jp2"

    band_nir_path = "C:/Users/debal/Downloads/L1C_T43REL_A008396_20170130T053159/S2A_MSIL1C_20170130T053041_N0204_R105_T43REL_20170130T053159.SAFE/GRANULE/L1C_T43REL_A008396_20170130T053159/IMG_DATA/T43REL_20170130T053041_B08.jp2"
    
    band_red_image_2017 = cv2.imread(band_red_path, cv2.IMREAD_GRAYSCALE)
    band_nir_image_2017 = cv2.imread(band_nir_path, cv2.IMREAD_GRAYSCALE)
    ndvi2017 = ndvi_generator.generateNDVI(band_red_image_2017, band_nir_image_2017)

    # #TempObjectStorage.storeMatrix(ndvi2017, "./temp/ndvi2017")

    # # Get the NDVI image from 2020
    band_red_path = "C:/Users/debal/Downloads/L1C_T43REL_A015146_20200130T053806/S2B_MSIL1C_20200130T053049_N0208_R105_T43REL_20200130T090639.SAFE/GRANULE/L1C_T43REL_A015146_20200130T053806/IMG_DATA/T43REL_20200130T053049_B04.jp2"

    band_red_image_2020 = cv2.imread(band_red_path, cv2.IMREAD_GRAYSCALE)
    band_nir_image_2020 = cv2.imread(band_nir_path, cv2.IMREAD_GRAYSCALE)

    band_red_image_2020 = cv2.imread(band_red_path, cv2.IMREAD_GRAYSCALE)
    band_nir_image_2020 = cv2.imread(band_nir_path, cv2.IMREAD_GRAYSCALE)

    ndvi2020 = ndvi_generator.generateNDVI(band_red_image_2020, band_nir_image_2020)

    # TempObjectStorage.storeMatrix(ndvi2020, "./temp/ndvi2020")

    

    # to run write - (Measure-Command { python main.py | Out-Default }).ToString()

    # Calculate the amount of healthy vegetation.
    # Healthy vegetation is considered to be those whose NDVI is more than 0.5
    # healthy2017 = 0
    # healthy2020 = 0
    # for row in range(ndvi2017.shape[0]):
    #     for column in range(ndvi2017.shape[1]):
    #         if(ndvi2017[row][column] >= 0.5):
    #             healthy2017 += 1
            
    #         if(ndvi2020[row][column] >= 0.5):
    #             healthy2020 += 1

    # # Calculate the change in the two
    # change_ndvi = ndvi2020 - ndvi2017

    # # Calculate the change in forest cover (NDVI)
    # total_pixels = change_ndvi.shape[0] * change_ndvi.shape[1]
    # no_change_pixels = 0
    # positive_change_pixels = 0
    # negative_change_pixels = 0

    # # Iterate over all the pixels and figure out where changes have been observed in NDVI
    # for row in range(change_ndvi.shape[0]):
    #     for column in range(change_ndvi.shape[1]):
    #         if(change_ndvi[row][column] == 0):
    #             no_change_pixels += 1
    #         elif(change_ndvi[row][column] > 0):
    #             positive_change_pixels += 1
    #         else:
    #             negative_change_pixels += 1

    # # Print the details calculated above
    # print(f"No Change Pixels = {(no_change_pixels / total_pixels) * 100.0}%")
    # print(f"Positive Change Pixels = {(positive_change_pixels / total_pixels) * 100.0}%")
    # print(f"Negative Change Pixels = {(negative_change_pixels / total_pixels) * 100.0}%")

    # print(f"Healthy Vegetation in 2017 = {(healthy2017 / total_pixels) * 100.0}%")
    # print(f"Healthy Vegetation in 2020 = {(healthy2020 / total_pixels) * 100.0}%")
    # print(f"Change in Vegetation = {((healthy2020 - healthy2017) / total_pixels) * 100.0}%")

    # ndvi2017 = TempObjectStorage.loadMatrix("./temp/ndvi2017.npy")
    # ndvi2020 = TempObjectStorage.loadMatrix("./temp/ndvi2020.npy")
    visualizations.visualizeNDVIContinuous(ndvi2017)

    visualizations.visualizeNDVICategorical(ndvi2020)
>>>>>>> 41e1c49444d96379b3488b6d4f30b256b5401644
