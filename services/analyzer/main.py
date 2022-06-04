import numpy as np
import os
from dotenv import load_dotenv
import mariadb

import generate_stats

load_dotenv()

if(__name__ == "__main__"):
    # Setup connection to database
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

    print("Choose an option below:")
    print("1. Generate statistics for a particular year")
    print("2. Generate statistics for the change between 2 years")
    print("3. Generate Inference for future time")
    choice_main = int(input("Choice: "))

    # Generate statistics for a particular year
    if(choice_main == 1):
        # Present the areas available for selection to the user
        cursor.execute("SELECT area_name FROM AREAS")
        areas = []

        for (area_name,) in cursor:
            areas.append(area_name)
        
        print("\nSelect an Area. The available options are as follows:")
        for index, area_name in enumerate(areas):
            print(f"{index + 1}. {area_name}")
        
        choice_area = int(input("Choice: "))

        # After the area has been chosen, present the years for which data is available for the chosen area
        cursor.execute(
            "SELECT date, ndvi_data_path FROM STORED_DATA_INFO WHERE area_id = (SELECT area_id FROM AREAS WHERE area_name = ?) AND ndvi_generated = ?",
            (areas[choice_area - 1], 1)
        )
        results = []

        for (date, ndvi_data_path) in cursor:
            results.append((date, ndvi_data_path))
        
        print("\nSelect a Date for which calculation is to be done:")
        for index, (date, ndvi_data_path) in enumerate(sorted(results, key = lambda x : x[0])):
            print(f"{index + 1}. {date.year} {date.strftime('%B')}")
        
        choice_date = int(input("Choice: "))

        # Generate the path to NDVI matrix corresponding to the year selected
        ndvi_matrix_path: str = results[choice_date - 1][1]

        # Load the NDVI matrix
        ndvi: np.ndarray = np.load(file = os.path.join(ndvi_matrix_path, "ndvi_matrix.npy"))

        # Calculate vegetation cover
        vegetation_stats = generate_stats.calculateVegetationCover(ndvi)

        # Sparse vegetation cover
        sparse_vegetation_percent = "{:.2f}".format(vegetation_stats[os.environ.get("NDVI_SPARSE_VEGETATION")] / vegetation_stats["total_pixels"] * 100)
        print(f"\nSparse Vegetation Cover: {sparse_vegetation_percent} %")

        # Moderate vegetation cover
        moderate_vegetation_percent = "{:.2f}".format(vegetation_stats[os.environ.get("NDVI_MODERATE_VEGETATION")] / vegetation_stats["total_pixels"] * 100)
        print(f"Moderate Vegetation Cover: {moderate_vegetation_percent} %")

        # Thick vegetation cover
        thick_vegetation_percent = "{:.2f}".format(vegetation_stats[os.environ.get("NDVI_THICK_VEGETATION")] / vegetation_stats["total_pixels"] * 100)
        print(f"Thick Vegetation Cover: {thick_vegetation_percent} %")

        # Total vegetated area
        total_vegetation = "{:.2f}".format((vegetation_stats[os.environ.get("NDVI_SPARSE_VEGETATION")] + vegetation_stats[os.environ.get("NDVI_MODERATE_VEGETATION")] + vegetation_stats[os.environ.get("NDVI_THICK_VEGETATION")]) / vegetation_stats["total_pixels"] * 100)
        print(f"\nVegetated Area: {total_vegetation} %")

        # Calculate land cover
        land_stats = generate_stats.calculateLandCover(ndvi)
        no_vegetation_percent = "{:.2f}".format(land_stats[os.environ.get("NDVI_NO_VEGETATION")] / land_stats["total_pixels"] * 100)
        print(f"Non Vegetated Area: {no_vegetation_percent} %")

        # Print the bar chart
        combined_stats = { **vegetation_stats, **land_stats }
        generate_stats.plotBarVegetation(combined_stats)
    

    # Generate statistics for the change between 2 years
    elif(choice_main == 2):
        # Present the areas available for selection to the user
        cursor.execute("SELECT area_name FROM AREAS")
        areas = []

        for (area_name,) in cursor:
            areas.append(area_name)
        
        print("\nSelect an Area. The available options are as follows:")
        for index, area_name in enumerate(areas):
            print(f"{index + 1}. {area_name}")
        
        choice_area = int(input("Choice: "))

        # After the area has been chosen, present the years for which data is available for the chosen area
        cursor.execute(
            "SELECT date, ndvi_data_path FROM STORED_DATA_INFO WHERE area_id = (SELECT area_id FROM AREAS WHERE area_name = ?) AND ndvi_generated = ?",
            (areas[choice_area - 1], 1)
        )
        results = []

        for (date, ndvi_data_path) in cursor:
            results.append((date, ndvi_data_path))
        
        choice_of_years = []
        print("\nSelect Dates for which calculation is to be done:")
        for index, (date, ndvi_data_path) in enumerate(sorted(results, key = lambda x : x[0])):
            print(f"{index + 1}. {date.year} {date.strftime('%B')}")
            choice_of_years.append(date.year)

        choice_date1 = int(input("Choice Date 1 (This is the previous date): "))
        choice_date2 = int(input("Choice Date 2 (This is the later date): "))

        # Generate the path to NDVI matrices corresponding to the year selected
        ndvi_matrix_path1: str = results[choice_date1 - 1][1]
        ndvi_matrix_path2: str = results[choice_date2 - 1][1]

        # Load the NDVI matrices
        ndvi_start: np.ndarray = np.load(file = os.path.join(ndvi_matrix_path1, "ndvi_matrix.npy"))
        ndvi_end: np.ndarray = np.load(file = os.path.join(ndvi_matrix_path2, "ndvi_matrix.npy"))

        # Calculate vegetation cover
        vegetation_stats_start = generate_stats.calculateVegetationCover(ndvi_start)
        vegetation_stats_end = generate_stats.calculateVegetationCover(ndvi_end)

        # Calculate change vegetation cover for sparse vegetation
        if(vegetation_stats_start[os.environ.get("NDVI_SPARSE_VEGETATION")] > vegetation_stats_end[os.environ.get("NDVI_SPARSE_VEGETATION")]):
            deforestation_or_reforestation = "\nSparse Vegetation Cover has decreased by"
        else:
            deforestation_or_reforestation = "\nSparse Vegetation Cover has increased by"

        change_in_vegetation_cover = abs(vegetation_stats_end[os.environ.get("NDVI_SPARSE_VEGETATION")] - vegetation_stats_start[os.environ.get("NDVI_SPARSE_VEGETATION")])
        percent_change = "{:.2f}".format(change_in_vegetation_cover / vegetation_stats_start[os.environ.get("NDVI_SPARSE_VEGETATION")] * 100)
        
        print(f"{deforestation_or_reforestation} {percent_change} %")

                
        # Calculate change vegetation cover for moderate vegetation
        if(vegetation_stats_start[os.environ.get("NDVI_MODERATE_VEGETATION")] > vegetation_stats_end[os.environ.get("NDVI_MODERATE_VEGETATION")]):
            deforestation_or_reforestation = "\nModerate Vegetation Cover has decreased by"
        else:
            deforestation_or_reforestation = "\nModerate Vegetation Cover has increased by"

        change_in_vegetation_cover = abs(vegetation_stats_end[os.environ.get("NDVI_MODERATE_VEGETATION")] - vegetation_stats_start[os.environ.get("NDVI_MODERATE_VEGETATION")])
        percent_change = "{:.2f}".format(change_in_vegetation_cover / vegetation_stats_start[os.environ.get("NDVI_MODERATE_VEGETATION")] * 100)
        
        print(f"{deforestation_or_reforestation} {percent_change} %")
        
        # Calculate change vegetation cover for thick vegetation
        if(vegetation_stats_start[os.environ.get("NDVI_THICK_VEGETATION")] > vegetation_stats_end[os.environ.get("NDVI_THICK_VEGETATION")]):
            deforestation_or_reforestation = "\nThick Vegetation Cover has decreased by"
        else:
            deforestation_or_reforestation = "\nThick Vegetation Cover has increased by"
            
        change_in_vegetation_cover = abs(vegetation_stats_end[os.environ.get("NDVI_THICK_VEGETATION")] - vegetation_stats_start[os.environ.get("NDVI_THICK_VEGETATION")])
        percent_change = "{:.2f}".format(change_in_vegetation_cover / vegetation_stats_start[os.environ.get("NDVI_THICK_VEGETATION")] * 100)
        print(f"{deforestation_or_reforestation} {percent_change} %")

        # Overall change in vegetation
        total_vegetation_start = vegetation_stats_start[os.environ.get("NDVI_SPARSE_VEGETATION")] + vegetation_stats_start[os.environ.get("NDVI_MODERATE_VEGETATION")] + vegetation_stats_start[os.environ.get("NDVI_THICK_VEGETATION")]
        total_vegetation_end = vegetation_stats_end[os.environ.get("NDVI_SPARSE_VEGETATION")] + vegetation_stats_end[os.environ.get("NDVI_MODERATE_VEGETATION")] + vegetation_stats_end[os.environ.get("NDVI_THICK_VEGETATION")]
        if(total_vegetation_start > total_vegetation_end):
            deforestation_or_reforestation = "\nTotal deforestation is"
        else:
            deforestation_or_reforestation = "\nTotal reforestation is"

        change_in_total_cover = "{:.2f}".format(abs(total_vegetation_end - total_vegetation_start) / total_vegetation_start * 100)
        print(f"{deforestation_or_reforestation} {change_in_total_cover} %")
        
        # Calculate land cover
        land_stats_start = generate_stats.calculateLandCover(ndvi_start)
        land_stats_end = generate_stats.calculateLandCover(ndvi_end)

        total_barren_start = land_stats_start[os.environ.get("NDVI_NO_VEGETATION")]
        total_barren_end = land_stats_end[os.environ.get("NDVI_NO_VEGETATION")]
        
        if(total_barren_start > total_barren_end):
            land_cover = "\nNon vegetated area has decreased by"
        else:
            land_cover = "\nNon vegetated area has increased by"

        change_in_no_vegetation_cover = "{:.2f}".format(abs(total_barren_end - total_barren_start) / total_barren_start *100)
        print(f"{land_cover} {change_in_no_vegetation_cover} %") 

        # Print the combined bar chart
        combined_stats_start = { **vegetation_stats_start, **land_stats_start }
        combined_stats_end = { **vegetation_stats_end, **land_stats_end }
        generate_stats.plotBarVegetationCombined(combined_stats_start, combined_stats_end, [choice_of_years[choice_date1-1], choice_of_years[choice_date2-1]])


    # Generate inference for future time
    elif(choice_main == 3):
        # Present the areas available for selection to the user
        cursor.execute("SELECT area_name FROM AREAS")
        areas = []

        for (area_name,) in cursor:
            areas.append(area_name)
        
        print("\nSelect an Area. The available options are as follows:")
        for index, area_name in enumerate(areas):
            print(f"{index + 1}. {area_name}")
        
        choice_area = int(input("Choice: "))

        # After the area has been chosen, get the years for which data is available for the chosen area
        cursor.execute(
            "SELECT date, ndvi_data_path FROM STORED_DATA_INFO WHERE area_id = (SELECT area_id FROM AREAS WHERE area_name = ?) AND ndvi_generated = ?",
            (areas[choice_area - 1], 1)
        )

        # This dictionary will be sent to the inference section to be converted into a Pandas dataframe.
        # This structure reflects the format expected by Prophet library - 2 columns, 1 for timestamp (ds)
        # and the other for the value to be predicted (y).
        prophet_compatible_dict = {
            "ds": [],
            "y": []
        }

        print("\nGenerating Vegetation Data for Images:")
        output_csv = "ds,y\n"

        for (date, ndvi_data_path) in cursor:
            # Ignore the 2022 data as it is not correct
            if(date.year == 2022):
                continue

            print(date)
            year = str(date)[0:4]
            month = str(date)[5:7]

            # Add the date to the dictionary
            prophet_compatible_dict["ds"].append(f"{year}-{month}")

            # We want to infer the amount of land under vegetation cover.
            # So we will only calculate forest cover.

            # Load the NDVI matrix
            ndvi: np.ndarray = np.load(file = os.path.join(ndvi_data_path, "ndvi_matrix.npy"))

            # Calculate vegetation cover
            vegetation_stats = generate_stats.calculateVegetationCover(ndvi)

            # Here, we consider only moderate and thick vegetation
            total_vegetation = vegetation_stats[os.environ.get("NDVI_MODERATE_VEGETATION")] + vegetation_stats[os.environ.get("NDVI_THICK_VEGETATION")]

            # Add this total vegetation to the dictionary
            prophet_compatible_dict["y"].append(total_vegetation)

            # Add data to CSV string
            output_csv += f"{year}-{month},{str(total_vegetation)}\n"
        
        # Output the CSV file for importing into the inference section
        with open("inference_csv.tmp.csv", "w") as file:
            file.write(output_csv)
        
        print("\nCSV file exported. Now run generate_inference.py from WSL to perform inference.")
        print("This is a workaround as the Prophet library used is not compatible with Windows.")
        print("This will be soon removed when the application will be ported to Docker.")
        
        # Send over dictionary for inference
        # This method will not work until application is ported to Docker.
        # Until then, call generate_inference manually from WSL.
        # generate_inference.infer(prophet_compatible_dict)