import cv2
import numpy as np

def visualizeRGB(band_red_image: np.ndarray, band_green_image: np.ndarray, band_blue_image: np.ndarray, filename: str = "rgb.jpg") -> None:
    # Convert the input matrix to 32 bit float number.
    # This is because the tonemap function only works with float32 numbers.
    # If number is not in float32 then an assertion error will be thrown telling that type should be
    # CV_32FC3. Here, the 32 refers to 32 bit; F refers to float; and 3 refers to 3 dimensions. This last
    # value signifies RGB images as all RGB images have 3 dimensions (or channels).
    band_red_image = band_red_image.astype(dtype = np.float32)
    band_green_image = band_green_image.astype(dtype = np.float32)
    band_blue_image = band_blue_image.astype(dtype = np.float32)

    # Merge the separate layers (Red, Green and Blue) into a single image
    # Here the orde is different because OpenCV works with BGR and not RGB
    rgb_image = cv2.merge([band_blue_image, band_green_image, band_red_image])

    # Create the tonemap and process the merged image
    tonemap = cv2.createTonemapReinhard(gamma = 0.5, intensity = 3.5)
    tonemapped_image = tonemap.process(rgb_image)

    # The tonemapping process converts the image to the range 0 - 1.
    # So we multiply this with 255 so that the range becomes 0 - 255.
    tonemapped_image = tonemapped_image * 255

    # The image is still in float32 form here, but the export function most probably manages that
    # and automatically converts it into uint8 before exporting.
    cv2.imwrite(filename, tonemapped_image)



# Function to visualize the NDVI image calculated.
# Input is a numpy array of the NDVI image (values ranging between -1 and 1).
# Output will be a JPG file.
def visualizeNDVIContinuous(ndvi_image: np.ndarray) -> np.ndarray:
    
    band_blue_image = np.zeros(ndvi_image.shape, dtype = np.float32)
    band_green_image = np.zeros(ndvi_image.shape, dtype = np.float32)
    band_red_image = np.zeros(ndvi_image.shape, dtype = np.float32)
    for row in range(ndvi_image.shape[0]):
        for column in range(ndvi_image.shape[1]):

            # Continuous
            # If the NDVI value is less than 0, then we consider no vegetation hence the nir band is mapped to the entire red band
            if(ndvi_image[row][column] < 0):
                band_red_image[row][column] = 255

            # If the NDVI value is greater than equal to 0 and less than 0.4, then we consider relatively less vegetation hence depending on the value of ndvi the colour varies from orange(ndvi 0) to yellow(ndvi 0.4)
            # The red band is fixed to 255
            #The value of green band varies from 150 to 255
            elif(ndvi_image[row][column] >= 0 and ndvi_image[row][column] < 0.4):    
                band_red_image[row][column] = 255
                band_green_image[row][column] = 150 + ndvi_image[row][column] * 262.5

            # If the NDVI value is greater than equal to 0.4, then we consider vegetation hence depending on the value of ndvi the colour varies from light green(ndvi 0.6) to deep green(ndvi 1)
            else:
                #The value of green band varies from 255 to 75
                band_green_image[row][column] = (1 - ndvi_image[row][column]) * 300 + 75
            
    final_ndvi_image = cv2.merge([band_blue_image, band_green_image, band_red_image])
            
    return final_ndvi_image


def visualizeNDVICategorical(ndvi_image: np.ndarray) -> np.ndarray:
    
    band_blue_image = np.zeros(ndvi_image.shape, dtype = np.float32)
    band_green_image = np.zeros(ndvi_image.shape, dtype = np.float32)
    band_red_image = np.zeros(ndvi_image.shape, dtype = np.float32)
    for row in range(ndvi_image.shape[0]):
        for column in range(ndvi_image.shape[1]):
         
            #Categorical
            # If the NDVI value is less than 0, then we consider no vegetation, hence the nir band is mapped to the entire red band 
            if(ndvi_image[row][column] <= -0.5):
                band_red_image[row][column] = 166
                band_green_image[row][column] = 97
                band_blue_image[row][column] = 26

            elif(ndvi_image[row][column] <= -0.25):
                band_red_image[row][column] = 223
                band_green_image[row][column] = 194
                band_blue_image[row][column] = 125

            # If the NDVI value is greater than equal to 0 and less than 0.2, then we consider almost negligible vegetation, hence the nir band is mapped to a mixture of red and green band (orange colour)
            elif(ndvi_image[row][column] <= 0.25):
                band_red_image[row][column] = 245
                band_green_image[row][column] = 245
                band_blue_image[row][column] = 245

            # If the NDVI value is greater than equal to 0.2 and less than 0.4, then we consider very low amount of vegetation, hence the nir band is mapped to a mixture of red and green band (yellow colour)
            elif(ndvi_image[row][column] <= 0.5):
                band_red_image[row][column] = 128
                band_green_image[row][column] = 205
                band_blue_image[row][column] = 193

            # If the NDVI value is greater than equal to 0.6, then we consider heavy vegetation, hence the nir band is mapped to green band (deep green colour)
            else:
                band_red_image[row][column] = 1
                band_green_image[row][column] = 133
                band_blue_image[row][column] = 113

    final_ndvi_image = cv2.merge([band_blue_image, band_green_image, band_red_image])
            
    return final_ndvi_image


# Function to visualize the change map obtained by differencing NDVI of two years.
# Input is a numpy array containing the change map (values ranging between -2 and 2).
# Output will be a JPG file.
def visualizeChangeMap(change_map: np.ndarray) -> None:
    pass



if(__name__ == "__main__"):
    # band_red_image = plt.imread("C:/Users/User/Downloads/L1C_T43REL_A008396_20170130T053159/S2A_MSIL1C_20170130T053041_N0204_R105_T43REL_20170130T053159.SAFE/GRANULE/L1C_T43REL_A008396_20170130T053159/IMG_DATA/T43REL_20170130T053041_B04.jp2")

    # band_green_image = plt.imread("C:/Users/User/Downloads/L1C_T43REL_A008396_20170130T053159/S2A_MSIL1C_20170130T053041_N0204_R105_T43REL_20170130T053159.SAFE/GRANULE/L1C_T43REL_A008396_20170130T053159/IMG_DATA/T43REL_20170130T053041_B03.jp2")

    # band_blue_image = plt.imread("C:/Users/User/Downloads/L1C_T43REL_A008396_20170130T053159/S2A_MSIL1C_20170130T053041_N0204_R105_T43REL_20170130T053159.SAFE/GRANULE/L1C_T43REL_A008396_20170130T053159/IMG_DATA/T43REL_20170130T053041_B02.jp2")

    # plt.imsave("./band.jpg", band_red_image)

    # visualizeRGB(band_red_image, band_green_image, band_blue_image)

    red = cv2.imread("C:/Users/User/Downloads/L1C_T43REL_A015146_20200130T053806/S2B_MSIL1C_20200130T053049_N0208_R105_T43REL_20200130T090639.SAFE/GRANULE/L1C_T43REL_A015146_20200130T053806/IMG_DATA/T43REL_20200130T053049_B04.jp2", cv2.IMREAD_GRAYSCALE)

    green = cv2.imread("C:/Users/User/Downloads/L1C_T43REL_A015146_20200130T053806/S2B_MSIL1C_20200130T053049_N0208_R105_T43REL_20200130T090639.SAFE/GRANULE/L1C_T43REL_A015146_20200130T053806/IMG_DATA/T43REL_20200130T053049_B03.jp2", cv2.IMREAD_GRAYSCALE)

    blue = cv2.imread("C:/Users/User/Downloads/L1C_T43REL_A015146_20200130T053806/S2B_MSIL1C_20200130T053049_N0208_R105_T43REL_20200130T090639.SAFE/GRANULE/L1C_T43REL_A015146_20200130T053806/IMG_DATA/T43REL_20200130T053049_B02.jp2", cv2.IMREAD_GRAYSCALE)

    visualizeRGB(red, green, blue)