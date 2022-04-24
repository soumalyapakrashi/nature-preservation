import matplotlib.pyplot as plt
import GPUtil

available_gpu_list = GPUtil.getAvailable()

if(len(available_gpu_list) == 0):
    gpu_available: bool = False
else:
    gpu_available: bool = True

gpu_available = False

if not gpu_available:
    import numpy as np
    np.seterr(invalid = "ignore")
else:
    import numpy as np
    import cupy as cp


def _computeOnGPU(band_red_image: np.ndarray, band_nir_image: np.ndarray):
    # band_red_image = cp.array(band_red_image, dtype = cp.int32)
    # band_nir_image = cp.array(band_nir_image, dtype = cp.int32)

    pass


def _computeOnCPU(band_red_image: np.ndarray, band_nir_image: np.ndarray) -> np.ndarray:
    band_red_image = band_red_image.astype(dtype = np.int32)
    band_nir_image = band_nir_image.astype(dtype = np.int32)

    ndvi_image = (band_nir_image - band_red_image) / (band_nir_image + band_red_image)

    # Substitute the NaN values
    for row in range(ndvi_image.shape[0]):
        for column in range(ndvi_image.shape[1]):
            if(np.isnan(ndvi_image[row][column])):
                ndvi_image[row][column] = 0.0
    
    # print(ndvi_image.max())
    # print(ndvi_image.min())

    return ndvi_image


def generateNDVI(band_red_path: str, band_nir_path: str) -> np.ndarray:
    band_red_image = plt.imread(band_red_path)
    band_nir_image = plt.imread(band_nir_path)

    if not gpu_available:
        ndvi_image = _computeOnCPU(band_red_image, band_nir_image)

    return ndvi_image
