import numpy as np
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
    import cupy as cp


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
    
    # Get the images which have not been processed.
    # Images that have not been processed will have a 0 in their 'ndvi_generated' field.
    # Else it will have a 1.
    cursor.execute("SELECT id, area_id, date, sat_data_path FROM STORED_DATA_INFO WHERE ndvi_generated = ?", (0,))

    # This will contain the information about every image calculated so that database can be updated accordingly
    database_update = []

    # Iterate over each tuple
    for (id, area_id, date, sat_data_path) in cursor:
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
            str(date)
        )

        # Store the matrix to object storage
        ObjectStorage.storeMatrix(ndvi, save_path, "ndvi_matrix.npy")

        database_update.append((id, save_path))

        # Generate NDVI image and overlay with colors according to continuous values
        ndvi_vis_continuous = visualizations.visualizeNDVIContinuous(ndvi)
        cv2.imwrite(os.path.join(save_path, "ndvi_continuous.jpg"), ndvi_vis_continuous)

        # Generate NDVI image and overlay with colors according to categorical values
        ndvi_vis_categorical = visualizations.visualizeNDVICategorical(ndvi)
        cv2.imwrite(os.path.join(save_path, "ndvi_categorical.jpg"), ndvi_vis_categorical)

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
