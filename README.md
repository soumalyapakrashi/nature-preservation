# Nature Preservation

## Contents

1. Setup
    1. Install Python and Virtualenv
    2. Setup XAMPP
    3. Setup GDAL
    4. Download the project
    5. Setup the environment variables
    6. Setup image-fetcher module
    7. Setup ndvi-generator module
    8. Setup analyzer module
    9. Setup database tables


## Setup

### Setup Python and Virtualenv

If Python 3 is not installed, install it from this [link](https://www.python.org/downloads/).

Check installation by running:

```shell
python --version
pip --version
```

If `pip` command does not work, try running:

```shell
python -m pip --version
```

If `virtualenv` is not installed, install it using following command:

```shell
pip install virtualenv
```

If it does not work, then

```shell
python -m pip install virtualenv
```


### Setup XAMPP

XAMPP is required to use the **MariaDB** database. To set it up, we first need to download and install it. It can be obtained from [here](https://www.apachefriends.org/index.html).


### Setup GDAL

GDAL is a command-line tool which is used for performing a number of Geospatial Calculations. We use this module here to perform cropping of image tiles to points of interest.

We first need to download it and install it from this [link](https://www.gisinternals.com/query.html?content=filelist&file=release-1930-x64-gdal-3-4-3-mapserver-7-6-4.zip). These links are only for Windows. There are versions available for Mac and Linux as well.

Considering GDAL has been installed in {GDAL_INSTALL_DIR}, the following environment variables need to be set:

```shell
PATH={GDAL_INSTALL_DIR}
GDAL_DATA={GDAL_INSTALL_DIR}/gdal-data
PROJ_LIB={GDAL_INSTALL_DIR}/projlib
```

After updating the environment variables, restart the computer and then verify the GDAL installation by running the following command in the terminal:

```shell
gdalwarp --version
```

The output should show the version number of GDAL installed and its release date.


### Download the project

Clone the repository in local computer.

```shell
git clone https://github.com/soumalyapakrashi/nature-preservation
```

Move into the project directory

```shell
cd nature-preservation
```

Create the directories which will be used as *Object Storage* for storing the required files. First create a directory called `storage` and within that, create 2 other directories called `satellite_data` and `ndvi_data`.

```shell
mkdir storage
cd storage
mkdir satellite_data
mkdir ndvi_data
```


### Setup the environment variables

Come back to the project root directory. Here, create a file called `.env` in which we will store all our project specific environment variables. Here, `{PROJECT_BASE_DIR}` is not any environment variable; it is just used as a reference to denote the base directory where all the files belonging to this project is present, that is, the directory where this .env file is created and all the other folders like *services* and *storage* reside.

Add the following environment variables:

1. MYSQL_USER - This refers to the username of the MariaDB database. If not changed, by default, this is `root`.

2. MYSQL_PASSWORD - This refers to the password of the MariaDB database. If not changed, by default it is a blank string.

3. MYSQL_HOST - If running on local machine, this will be `localhost`.

4. MYSQL_PORT - This can be obtained from the XAMPP control panel.

5. MYSQL_DATABASE - Set this to `nature_preservation`.

6. NDVI_STORAGE_BASE_DIR - Set this to `{PROJECT_BASE_DIR}/storage/ndvi_data`.

7. NDVI_THICK_VEGETATION - These are the set of variables which denote the levels how NDVI data is interpreted. This can be modified as required. Set this to `0.6`. It is interpreted as any NDVI value greater than or equal to 0.6, will be considered thick vegetation.

8. NDVI_MODERATE_VEGETATION - Set this to `0.4`. This can be interpreted as any NDVI value greater than or equal to 0.4 and less than 0.6 will be considered moderate vegetation. All other values are also interpreted similarly.

9. NDVI_SPARSE_VEGETATION - Set this to `0.1`.

10. NDVI_NO_VEGETATION - Set this to `-0.25`.

11. NDVI_BARREN - Set this to `-1.0`.


### Setup image-fetcher module

Move into the `image-fetcher` module directory from the project base directory.

```shell
cd services/image-fetcher
```

Create a new virtual environment.

```shell
virtualenv venv
```

If above command does not work, try this.

```shell
python -m virtualenv venv
```

Then, activate the virtual environment.

```shell
venv/Scripts/activate
```

Install the dependencies from the `requirements.txt` file.

```shell
pip install -r requirements.txt
```

Finally, deactivate the environment.

```shell
deactivate
```


### Setup ndvi-generator module

Similar to the `image-fetcher` module, set up the `ndvi-generator` module. The commands are run one at a time, assuming from the base project directory.

```shell
cd services/ndvi-generator
virtualenv venv
venv/Scripts/activate
pip install -r requirements.txt
deactivate
```


### Setup analyzer module

Similarly, set up the `analyzer` module. The commands are run one at a time, assuming from the base project directory.

```shell
cd services/analyzer
virtualenv venv
venv/Scripts/activate
pip install -r requirements.txt
deactivate
```


### Setup database tables

Finally add the required tables to the database. Open PHPMyAdmin by visiting `localhost/phpmyadmin`. From here, either run [db_setup.sql](./services/database/db_setup.sql) file, or perform the operations as stated in the file manually.

Steps to perform to manually setup the database include:

1. Create a database named `nature_preservation`.
2. Select the database.
3. Create the two tables `AREAS` and `STORED_DATA_INFO` as given in [db_setup.sql](./services/database/db_setup.sql) in the *Query Editor*.
