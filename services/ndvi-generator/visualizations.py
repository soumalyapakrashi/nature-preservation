import cv2
import numpy as np
import matplotlib.pyplot as plt

def visualizeRGB(band_red_image, band_green_image, band_blue_image) -> None:
    # rgb_image = np.dstack((band_red_image, band_green_image, band_blue_image))
    rgb_image = cv2.merge([band_blue_image, band_green_image, band_red_image])

    tonemap = cv2.createTonemapDrago(gamma = 1.0)
    tonemapped_image = tonemap.process(rgb_image)
    # image_8bit = np.clip(tonemapped_image * 255, 0, 255).astype('uint8')
    # cv2.imshow("RGB", image_8bit)
    # cv2.waitKey(0)
    cv2.imwrite("tonemapped.jpg", tonemapped_image)



# Function to visualize the NDVI image calculated.
# Input is a numpy array of the NDVI image (values ranging between -1 and 1).
# Output will be a JPG file.
def visualizeNDVI(ndvi_image: np.ndarray, name: str = "ndvi.jpg") -> None:
    pass



# Function to visualize the change map obtained by differencing NDVI of two years.
# Input is a numpy array containing the change map (values ranging between -2 and 2).
# Output will be a JPG file.
def visualizeChangeMap(change_map: np.ndarray, name: str = "change_map.jpg") -> None:
    pass



if(__name__ == "__main__"):
    # band_red_image = plt.imread("C:/Users/User/Downloads/L1C_T43REL_A008396_20170130T053159/S2A_MSIL1C_20170130T053041_N0204_R105_T43REL_20170130T053159.SAFE/GRANULE/L1C_T43REL_A008396_20170130T053159/IMG_DATA/T43REL_20170130T053041_B04.jp2")

    # band_green_image = plt.imread("C:/Users/User/Downloads/L1C_T43REL_A008396_20170130T053159/S2A_MSIL1C_20170130T053041_N0204_R105_T43REL_20170130T053159.SAFE/GRANULE/L1C_T43REL_A008396_20170130T053159/IMG_DATA/T43REL_20170130T053041_B03.jp2")

    # band_blue_image = plt.imread("C:/Users/User/Downloads/L1C_T43REL_A008396_20170130T053159/S2A_MSIL1C_20170130T053041_N0204_R105_T43REL_20170130T053159.SAFE/GRANULE/L1C_T43REL_A008396_20170130T053159/IMG_DATA/T43REL_20170130T053041_B02.jp2")

    # visualizeRGB(band_red_image, band_green_image, band_blue_image)

    red = cv2.imread("C:/Users/User/Downloads/L1C_T43REL_A015146_20200130T053806/S2B_MSIL1C_20200130T053049_N0208_R105_T43REL_20200130T090639.SAFE/GRANULE/L1C_T43REL_A015146_20200130T053806/IMG_DATA/T43REL_20200130T053049_B04.jp2", cv2.IMREAD_GRAYSCALE)

    green = cv2.imread("C:/Users/User/Downloads/L1C_T43REL_A015146_20200130T053806/S2B_MSIL1C_20200130T053049_N0208_R105_T43REL_20200130T090639.SAFE/GRANULE/L1C_T43REL_A015146_20200130T053806/IMG_DATA/T43REL_20200130T053049_B03.jp2", cv2.IMREAD_GRAYSCALE)

    blue = cv2.imread("C:/Users/User/Downloads/L1C_T43REL_A015146_20200130T053806/S2B_MSIL1C_20200130T053049_N0208_R105_T43REL_20200130T090639.SAFE/GRANULE/L1C_T43REL_A015146_20200130T053806/IMG_DATA/T43REL_20200130T053049_B02.jp2", cv2.IMREAD_GRAYSCALE)

    visualizeRGB(red, green, blue)