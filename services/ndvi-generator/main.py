import ndvi_generator

if(__name__ == "__main__"):
    # Get the NDVI images from Sentinel 2017 and 2020
    ndvi2017 = ndvi_generator.generateNDVI(
        band_red_path = "C:/Users/User/Downloads/L1C_T43REL_A008396_20170130T053159/S2A_MSIL1C_20170130T053041_N0204_R105_T43REL_20170130T053159.SAFE/GRANULE/L1C_T43REL_A008396_20170130T053159/IMG_DATA/T43REL_20170130T053041_B04.jp2",

        band_nir_path = "C:/Users/User/Downloads/L1C_T43REL_A008396_20170130T053159/S2A_MSIL1C_20170130T053041_N0204_R105_T43REL_20170130T053159.SAFE/GRANULE/L1C_T43REL_A008396_20170130T053159/IMG_DATA/T43REL_20170130T053041_B08.jp2"
    )

    ndvi2020 = ndvi_generator.generateNDVI(
        band_red_path = "C:/Users/User/Downloads/L1C_T43REL_A015146_20200130T053806/S2B_MSIL1C_20200130T053049_N0208_R105_T43REL_20200130T090639.SAFE/GRANULE/L1C_T43REL_A015146_20200130T053806/IMG_DATA/T43REL_20200130T053049_B04.jp2",

        band_nir_path = "C:/Users/User/Downloads/L1C_T43REL_A015146_20200130T053806/S2B_MSIL1C_20200130T053049_N0208_R105_T43REL_20200130T090639.SAFE/GRANULE/L1C_T43REL_A015146_20200130T053806/IMG_DATA/T43REL_20200130T053049_B08.jp2"
    )

    # Calculate the change in the two
    ndvi2017 = ndvi2017 + 1
    ndvi2020 = ndvi2020 + 1
    change_ndvi = ndvi2020 - ndvi2017

    # Calculate the change in forest cover (NDVI)
    total_pixels = change_ndvi.shape[0] * change_ndvi.shape[1]
    no_change_pixels = 0
    positive_change_pixels = 0
    negative_change_pixels = 0

    for row in range(change_ndvi.shape[0]):
        for column in range(change_ndvi.shape[1]):
            if(change_ndvi[row][column] == 0):
                no_change_pixels += 1
            elif(change_ndvi[row][column] > 0):
                positive_change_pixels += 1
            else:
                negative_change_pixels += 1
    
    print(f"No Change Pixels = {(no_change_pixels / total_pixels) * 100.0}%")
    print(f"Positive Change Pixels = {(positive_change_pixels / total_pixels) * 100.0}%")
    print(f"Negative Change Pixels = {(negative_change_pixels / total_pixels) * 100.0}%")
    