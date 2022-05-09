-- Create a new database with the name 'nature-preservation'
CREATE DATABASE nature_preservation;

-- Select the newly created database
USE nature_preservation;

-- This table will contain the areas in which we have data available in our repertoire
CREATE TABLE AREAS(
    area_id INT AUTO_INCREMENT,
    area_name VARCHAR(255) NOT NULL,
    PRIMARY KEY(area_id)
);

-- This table contains information about what years of data are available per area,
-- Where the raw satellite data are available and where the processed NDVI data are available
CREATE TABLE STORED_DATA_INFO(
    id INT AUTO_INCREMENT,
    area_id INT REFERENCES AREAS(area_id),
    year YEAR NOT NULL,
    sat_data_path VARCHAR(255) NOT NULL,
    ndvi_generated TINYINT DEFAULT 0,
    ndvi_data_path VARCHAR(255),
    PRIMARY KEY(id)
);
