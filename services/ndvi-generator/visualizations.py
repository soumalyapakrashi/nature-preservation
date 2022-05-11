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
            if(ndvi_image[row][column] < 0):
                band_red_image[row][column] = 255

            # If the NDVI value is greater than equal to 0 and less than 0.2, then we consider almost negligible vegetation, hence the nir band is mapped to a mixture of red and green band (orange colour)
            elif(ndvi_image[row][column] >= 0 and ndvi_image[row][column] < 0.2):
                band_red_image[row][column] = 255
                band_green_image[row][column] = 150

            # If the NDVI value is greater than equal to 0.2 and less than 0.4, then we consider very low amount of vegetation, hence the nir band is mapped to a mixture of red and green band (yellow colour)
            elif(ndvi_image[row][column] >= 0.2 and ndvi_image[row][column] < 0.4):
                band_red_image[row][column] = 255
                band_green_image[row][column] = 255

            # If the NDVI value is greater than equal to 0.4 and less than 0.6, then we consider light vegetation, hence the nir band is mapped to green band (light green colour)
            elif(ndvi_image[row][column] >= 0.4 and ndvi_image[row][column] < 0.6):
                band_green_image[row][column] = 255

            # If the NDVI value is greater than equal to 0.6, then we consider heavy vegetation, hence the nir band is mapped to green band (deep green colour)
            else:
                band_green_image[row][column] = 100

    final_ndvi_image = cv2.merge([band_blue_image, band_green_image, band_red_image])
            
    return final_ndvi_image
