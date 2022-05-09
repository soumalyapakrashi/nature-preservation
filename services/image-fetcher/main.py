import argparse
import os
import shutil
import subprocess

parser = argparse.ArgumentParser()

if(__name__ == "__main__"):
    # Add the arguments for loading new data
    parser.add_argument(
        "--area",
        required = True,
        help = "Area where the input image belongs"
    )

    parser.add_argument(
        "--year",
        required = True,
        help = "Year in which the image was taken"
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

    # Generate the output path
    output_path = os.path.join("D:/Programs/nature-preservation/storage/satellite_data", args.area, args.year)
    os.makedirs(output_path, exist_ok = True)

    # Iterate over the images in the input path and copy the images to the output path.
    # In the process, if crop coordinates are specified, then crop the images and copy.
    for image in os.listdir(args.image_path):
        if(args.crop_coords):
            # Convert the coords list from string to floats
            # crop_coords = list(map(float, args.crop_coords))

            # Copy only bands 2, 3, 4, and 8
            if(image.endswith("B02.jp2") or image.endswith("B03.jp2") or image.endswith("B04.jp2") or image.endswith("B08.jp2")):
                command = ["gdalwarp", "-te"]
                for coord in args.crop_coords:
                    command.append(coord)
                command.append("-te_srs")
                command.append("EPSG:4326")
                command.append("-t_srs")
                command.append("EPSG:3857")
                command.append(os.path.join(args.image_path, image))
                command.append(os.path.join(output_path, image))

                # print(command)

                subprocess.run(
                    command,
                    capture_output = True,
                    text = True
                )
        
        else:
            # Copy only bands 2, 3, 4, and 8
            if(image.endswith("B02.jp2") or image.endswith("B03.jp2") or image.endswith("B04.jp2") or image.endswith("B08.jp2")):
                shutil.copy2(os.path.join(args.image_path, image), output_path)
