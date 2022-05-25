import os
import numpy as np
import matplotlib.pyplot as plt
from dotenv import load_dotenv

load_dotenv()

# Function calculates the percentages of vegetated land cover
def calculateVegetationCover(ndvi: np.ndarray) -> dict[str: float]:
    # Counters
    thick_vegetation = 0
    moderate_vegetation = 0
    sparse_vegetation = 0

    # Iterate over all the pixels and increment appropriate counters
    for row in range(ndvi.shape[0]):
        for column in range(ndvi.shape[1]):
            if(ndvi[row][column] >= float(os.environ.get("NDVI_THICK_VEGETATION"))):
                thick_vegetation += 1
            elif(ndvi[row][column] >= float(os.environ.get("NDVI_MODERATE_VEGETATION"))):
                moderate_vegetation += 1
            elif(ndvi[row][column] >= float(os.environ.get("NDVI_SPARSE_VEGETATION"))):
                sparse_vegetation += 1
    
    # Construct a dictionary with the above statistics
    vegetation_dict = {
        os.environ.get("NDVI_SPARSE_VEGETATION"): sparse_vegetation,
        os.environ.get("NDVI_MODERATE_VEGETATION"): moderate_vegetation,
        os.environ.get("NDVI_THICK_VEGETATION"): thick_vegetation,
        "total_pixels": ndvi.shape[0] * ndvi.shape[1]
    }
    
    return vegetation_dict


# Function calculates the percentages of non-vegetated regions
def calculateLandCover(ndvi: np.ndarray) -> dict[str: float]:
    # Counters
    no_vegetation = 0
    barren = 0

    # Again, iterate over all the pixels and update appropriate counters
    for row in range(ndvi.shape[0]):
        for column in range(ndvi.shape[1]):
            if(ndvi[row][column] < float(os.environ.get("NDVI_SPARSE_VEGETATION")) and 
                ndvi[row][column] >= float(os.environ.get("NDVI_NO_VEGETATION"))):
                no_vegetation += 1
            elif(ndvi[row][column] >= float(os.environ.get("NDVI_BARREN")) and
                ndvi[row][column] < float(os.environ.get("NDVI_NO_VEGETATION"))):
                barren += 1
    
    # Construct a dictionary from the above statistics
    land_dict = {
        os.environ.get("NDVI_BARREN"): barren,
        os.environ.get("NDVI_NO_VEGETATION"): no_vegetation,
        "total_pixels": ndvi.shape[0] * ndvi.shape[1]
    }
    
    return land_dict


# Function to plot a bar graph of the different classes of land cover.
# The classes are thick vegetation, moderate vegetation, sparse vegetation,
# no vegetation and barren.
def plotBarVegetation(class_frequencies: dict[str: float]) -> None:
    # Process the data to be shown
    names = ["Thick Vegetation", "Moderate Vegetation", "Sparse Vegetation", "No Vegetation", "Barren"]
    values = [
        class_frequencies[os.environ.get("NDVI_THICK_VEGETATION")] / class_frequencies["total_pixels"] * 100.0,
        class_frequencies[os.environ.get("NDVI_MODERATE_VEGETATION")] / class_frequencies["total_pixels"] * 100.0,
        class_frequencies[os.environ.get("NDVI_SPARSE_VEGETATION")] / class_frequencies["total_pixels"] * 100.0,
        class_frequencies[os.environ.get("NDVI_NO_VEGETATION")] / class_frequencies["total_pixels"] * 100.0,
        class_frequencies[os.environ.get("NDVI_BARREN")] / class_frequencies["total_pixels"] * 100.0
    ]

    # Figure size
    figure, axis = plt.subplots(figsize = (16, 9))

    # Horizontal bar plot
    axis.barh(names, values)

    # Remove axes splines
    for spline in ("top", "bottom", "left", "right"):
        axis.spines[spline].set_visible(False)

    # Set x label
    axis.set_xlabel("Landcover (in %)")

    # Add padding between axes and labels
    axis.xaxis.set_tick_params(pad = 5)
    axis.yaxis.set_tick_params(pad = 10)

    # Add x, y gridlines
    axis.grid(b = True, color ="grey", linestyle ="-.", linewidth = 0.5, alpha = 0.7)

    # Show top values
    axis.invert_yaxis()

    # Add annotation to bars
    for i in axis.patches:
        plt.text(
            i.get_width() + 0.2,
            i.get_y() + 0.5,
            str(round((i.get_width()), 2)),
            fontsize = 10,
            fontweight ="bold",
            color ="grey"
        )
    
    # Add Plot Title
    axis.set_title("Vegetation Cover", loc ="left")

    # Output the plot
    filename = "vegetation_bar.tmp.png"
    plt.savefig(filename)

    # Print the output location to terminal so that it can be accessed easily
    print(f"Histogram: {os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)}")


# Function to plot a combined bar graph at different times of the different classes of land cover.
# The classes are thick vegetation, moderate vegetation, sparse vegetation,
# no vegetation and barren.
def plotBarVegetationCombined(class_frequencies1: dict[str: float], class_frequencies2: dict[str: float], year_input: list) -> None:
    # Process the data to be shown
    year_input = [str(x) for x in year_input]
    names = ["Thick Vegetation "+year_input[0], "Thick Vegetation "+year_input[1], "Moderate Vegetation "+year_input[0], "Moderate Vegetation "+year_input[1], "Sparse Vegetation "+year_input[0], "Sparse Vegetation "+year_input[1], "No Vegetation "+year_input[0], "No Vegetation "+year_input[1], "Barren "+year_input[0], "Barren "+year_input[1]]
    values = [
        class_frequencies1[os.environ.get("NDVI_THICK_VEGETATION")] / class_frequencies1["total_pixels"] * 100.0,
        class_frequencies2[os.environ.get("NDVI_THICK_VEGETATION")] / class_frequencies2["total_pixels"] * 100.0,
        class_frequencies1[os.environ.get("NDVI_MODERATE_VEGETATION")] / class_frequencies1["total_pixels"] * 100.0,
        class_frequencies2[os.environ.get("NDVI_MODERATE_VEGETATION")] / class_frequencies2["total_pixels"] * 100.0,
        class_frequencies1[os.environ.get("NDVI_SPARSE_VEGETATION")] / class_frequencies1["total_pixels"] * 100.0,
        class_frequencies2[os.environ.get("NDVI_SPARSE_VEGETATION")] / class_frequencies2["total_pixels"] * 100.0,
        class_frequencies1[os.environ.get("NDVI_NO_VEGETATION")] / class_frequencies1["total_pixels"] * 100.0,
        class_frequencies2[os.environ.get("NDVI_NO_VEGETATION")] / class_frequencies2["total_pixels"] * 100.0,
        class_frequencies1[os.environ.get("NDVI_BARREN")] / class_frequencies1["total_pixels"] * 100.0,
        class_frequencies2[os.environ.get("NDVI_BARREN")] / class_frequencies2["total_pixels"] * 100.0
    ]

    # Figure size
    figure, axis = plt.subplots(figsize = (16, 9))

    # Horizontal bar plot
    colors=['blue', 'orange']
    axis.barh(names, values, color = colors)
    # plt.bar(names, values, color = "blue")

    # Remove axes splines
    for spline in ("top", "bottom", "left", "right"):
        axis.spines[spline].set_visible(False)

    # Set x label
    axis.set_xlabel("Landcover (in %)")

    # Add padding between axes and labels
    axis.xaxis.set_tick_params(pad = 5)
    axis.yaxis.set_tick_params(pad = 5)

    # Add x, y gridlines
    axis.grid(b = True, color ="grey", linestyle ="-.", linewidth = 0.5, alpha = 0.7)

    # Show top values
    axis.invert_yaxis()

    # Add annotation to bars
    for i in axis.patches:
        plt.text(
            i.get_width() + 0.2,
            i.get_y() + 0.5,
            str(round((i.get_width()), 2)),
            fontsize = 10,
            fontweight ="bold",
            color ="grey"
        )
    
    # Add Plot Title
    axis.set_title("Vegetation Cover", loc ="left")

    # Output the plot
    filename = "vegetation_bar_combined.tmp.png"
    plt.savefig(filename)

    # Print the output location to terminal so that it can be accessed easily
    print(f"Histogram: {os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)}")
