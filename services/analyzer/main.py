import numpy as np
import os
from dotenv import load_dotenv
import mariadb
import datetime

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
        print(f"\nVegetation Cover: {vegetation_stats}")

        # Calculate land cover
        land_stats = generate_stats.calculateLandCover(ndvi)
        print(f"Land Cover: {land_stats}")

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
            python_date = datetime(date[0:4], date[5:7], date[8:10])
            results.append((python_date, ndvi_data_path))
        
        print("\nSelect Dates for which calculation is to be done:")
        for index, (date, ndvi_data_path) in enumerate(sorted(results, key = lambda x : x[0])):
            print(f"{index + 1}. {date.year} {date.strftime('%B')}")
        
        choice_date1 = int(input("Choice Date 1 (This is the previous date): "))
        choice_date2 = int(input("Choice Date 2 (This is the later date): "))

        # Generate the path to NDVI matrices corresponding to the year selected
        ndvi_matrix_path1: str = results[choice_date1 - 1][1]
        ndvi_matrix_path2: str = results[choice_date2 - 1][1]

        # Load the NDVI matrices
        ndvi_start: np.ndarray = np.load(file = os.path.join(ndvi_matrix_path1, "ndvi_matrix.npy"))
        ndvi_end: np.ndarray = np.load(file = os.path.join(ndvi_matrix_path2, "ndvi_matrix.npy"))

        # Calculate the change
        change = ndvi_end - ndvi_start
