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
class TempObjectStorage:
    @staticmethod
    def storeMatrix(matrix: np.ndarray, filename: str) -> None:
        np.save(file = filename, arr = matrix)
    
    @staticmethod
    def loadMatrix(filename: str) -> np.ndarray:
        loaded_matrix: np.ndarray = np.load(file = filename)
        return loaded_matrix


if(__name__ == "__main__"):
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
    cursor.execute("SELECT id, area_id, year, sat_data_path FROM STORED_DATA_INFO WHERE ndvi_generated = 0")

    # Iterate over each tuple
    for (id, area_id, year, sat_data_path) in cursor:
        # Generate the path to the image files
        temp_path = os.path.join(
            sat_data_path,
            "GRANULE"
        )

        final_path = os.path.join(
            temp_path,
            os.listdir(temp_path)[0],
            "IMG_DATA"
        )

        # List all the image files in the required directory
        image_files = os.listdir(final_path)

        # Iterate over all the image files and choose only bands 4 and 8.
        # Load the chosen images using OpenCV.
        for image_file in image_files:
            if(image_file.endswith("B04.jp2")):
                band_red_image = cv2.imread(os.path.join(final_path, image_file), cv2.IMREAD_GRAYSCALE)

            elif(image_file.endswith("B08.jp2")):
                band_nir_image = cv2.imread(os.path.join(final_path, image_file), cv2.IMREAD_GRAYSCALE)

        # Generate the NDVI matrix.
        # This ndvi variable will be a np.ndarray if no GPU is available.
        # But if GPU is available, then it will be cp.ndarray.
        ndvi = ndvi_generator.generateNDVI(band_red_image, band_nir_image)

        if(gpu_available == True):
            del ndvi
            cp.get_default_memory_pool().free_all_blocks()
