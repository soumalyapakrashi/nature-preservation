import cv2
import os
import numpy as np

# NOTE: The following method is not used anywhere. This is just a prototype. This feature will be
# implemented in some later versions of the software. Please ignore this for documentation or
# presentation purposes.

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



# NOTE: The following method is not used anywhere as it is not relevant to our project as of now.
# This feature might be used in some later versions of the software. Please ignore this for
# documentation or presentation purposes.

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


# This function produces a visualisation (image) of the NDVI matrix by assigning distinct
# colors to each of the 4 categories of NDVI values defined in the .env file.
def visualizeNDVICategorical(ndvi_image: np.ndarray) -> np.ndarray:
    
    band_blue_image = np.zeros(ndvi_image.shape, dtype = np.float32)
    band_green_image = np.zeros(ndvi_image.shape, dtype = np.float32)
    band_red_image = np.zeros(ndvi_image.shape, dtype = np.float32)
    for row in range(ndvi_image.shape[0]):
        for column in range(ndvi_image.shape[1]):
         
            #Categorical

            # If heavy vegetation, a deep green colour is chosen
            if(ndvi_image[row][column] >= float(os.environ.get("NDVI_THICK_VEGETATION"))):
                band_red_image[row][column] = 1
                band_green_image[row][column] = 133
                band_blue_image[row][column] = 113
            
            # If moderate vegetation, a light green colour is chosen
            elif(ndvi_image[row][column] >= float(os.environ.get("NDVI_MODERATE_VEGETATION"))):
                band_red_image[row][column] = 128
                band_green_image[row][column] = 205
                band_blue_image[row][column] = 193
            
            # If sparse vegetation, a white colour is chosen
            elif(ndvi_image[row][column] >= float(os.environ.get("NDVI_SPARSE_VEGETATION"))):
                band_red_image[row][column] = 245
                band_green_image[row][column] = 245
                band_blue_image[row][column] = 245
            
            # If no vegetation, a light brown colour is chosen
            elif(ndvi_image[row][column] >= float(os.environ.get("NDVI_NO_VEGETATION"))):
                band_red_image[row][column] = 223
                band_green_image[row][column] = 194
                band_blue_image[row][column] = 125

                # This is a dark brown colour which goes well with this color scheme.
                # It is not required for this purpose as we are only interested with vegetation.
                # But it has been kept here so that in the future, if a new class needs to be added
                # which is on the negative NDVI scale, then this color can be used.
                # band_red_image[row][column] = 166
                # band_green_image[row][column] = 97
                # band_blue_image[row][column] = 26      

    final_ndvi_image = cv2.merge([band_blue_image, band_green_image, band_red_image])
            
    return final_ndvi_image
