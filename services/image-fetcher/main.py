import argparse
import os
import shutil
import subprocess
from dotenv import load_dotenv
import mariadb

load_dotenv()

parser = argparse.ArgumentParser()

if(__name__ == "__main__"):
    # Add the arguments for loading new data
    parser.add_argument(
        "--area",
        required = True,
        help = "Area where the input image belongs"
    )

    parser.add_argument(
        "--date",
        required = True,
        help = "Date on which the image was taken. The format should be YYYY-MM-DD"
    )

    parser.add_argument(
        "--image_path",
        required = True,
        help = "Path where the input image is located"
    )

    parser.add_argument(
        "--crop_coords",
        help = "Coordinates to crop image to",
        nargs = '+'
    )

    args = parser.parse_args()

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

    # Generate the output path
    output_path = os.path.join(os.environ.get("SAT_STORAGE_BASE_DIR"), args.area, args.date)
    os.makedirs(output_path, exist_ok = True)

    # Iterate over the images in the input path and copy the images to the output path.
    # In the process, if crop coordinates are specified, then crop the images and copy.
    for image in os.listdir(args.image_path):
        if(args.crop_coords):
            # Convert the coords list from string to floats
            # crop_coords = list(map(float, args.crop_coords))

            # Copy only bands 2, 3, 4, and 8
            if(image.endswith("B02.jp2") or image.endswith("B03.jp2") or image.endswith("B04.jp2") or image.endswith("B08.jp2")):
                # Generate the command to be executed
                command = ["gdalwarp", "-te"]
                for coord in args.crop_coords:
                    command.append(coord)
                command.append("-te_srs")
                command.append("EPSG:4326")
                command.append("-t_srs")
                command.append("EPSG:3857")
                command.append(os.path.join(args.image_path, image))
                command.append(os.path.join(output_path, image))

                # Execute the command
                subprocess.run(
                    command,
                    capture_output = True,
                    text = True,
                    check = True
                )
        
        else:
            # Copy only bands 2, 3, 4, and 8
            if(image.endswith("B02.jp2") or image.endswith("B03.jp2") or image.endswith("B04.jp2") or image.endswith("B08.jp2")):
                shutil.copy2(os.path.join(args.image_path, image), output_path)
        
    
    # Add the area to database if not already present
    cursor.execute("SELECT area_id FROM AREAS WHERE area_name = ?", (args.area,))

    rowcount = 0
    for (area_id,) in cursor:
        rowcount += 1

    if(rowcount == 0):
        cursor.execute("INSERT INTO AREAS (area_name) VALUES (?)", (args.area,))
        area_id = cursor.lastrowid
    else:
        for (id,) in cursor:
            area_id = id
    
    # Add the new image path data to database
    cursor.execute(
        "INSERT INTO STORED_DATA_INFO (area_id, date, sat_data_path) VALUES (?, ?, ?)",
        (area_id, args.date, output_path)
    )

    # Commit the changes made to the database
    connection.commit()

    # Close the connection to the database
    connection.close()
