import GPUtil
import numpy as np
import cupy as cp
np.seterr(invalid = "ignore")

# Check if GPU is available and set flag accordingly
available_gpu_list = GPUtil.getAvailable()

if(len(available_gpu_list) == 0):
    gpu_available: bool = False
else:
    gpu_available: bool = True


# Function to calculate NDVI on the GPU
def _computeOnGPU(band_red_image: np.ndarray, band_nir_image: np.ndarray) -> cp.ndarray:
    # Load the images into GPU memory
    band_red_image = cp.array(band_red_image, dtype = cp.int32)
    band_nir_image = cp.array(band_nir_image, dtype = cp.int32)

    # Calculate NDVI matrix
    ndvi_image = (band_nir_image - band_red_image) / (band_nir_image + band_red_image)

    # Substitute the NaN values with -1
    cp.nan_to_num(ndvi_image, copy = False, nan = -1.0)

    # Delete arrays which are not required any more
    del band_red_image
    del band_nir_image
    cp.get_default_memory_pool().free_all_blocks()

    return ndvi_image


# Function to calculate NDVI on the CPU
def _computeOnCPU(band_red_image: np.ndarray, band_nir_image: np.ndarray) -> np.ndarray:
    band_red_image = band_red_image.astype(dtype = np.int32)
    band_nir_image = band_nir_image.astype(dtype = np.int32)

    # Calculate NDVI
    ndvi_image = (band_nir_image - band_red_image) / (band_nir_image + band_red_image)

    # Substitute the NaN values with -1
    np.nan_to_num(ndvi_image, copy = False, nan = -1.0)

    return ndvi_image


def generateNDVI(band_red_image: np.ndarray, band_nir_image: np.ndarray) -> np.ndarray:

    if not gpu_available:
        ndvi_image = _computeOnCPU(band_red_image, band_nir_image)
    else:
        ndvi_image = _computeOnGPU(band_red_image, band_nir_image)

    return ndvi_image
