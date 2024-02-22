import numpy as np
import pandas as pd
import subprocess

import PIL.Image
from PIL.ExifTags import TAGS

from python.model.FileSystemNodeModel import File


class Image(File):

    def __init__(self, path: str, cache):
        super().__init__(path, cache)
        self._width = None
        self._height = None
        self._coords = None
        self._location = None
        self._populate_image_metadata()

    @property
    def width(self):
        """Return the width of the image."""
        return self._width

    @width.setter
    def width(self, value: int):
        self._width = value

    @property
    def height(self):
        """Return the height of the image."""
        return self._height

    @height.setter
    def height(self, value: int):
        self._height = value

    @property
    def coords(self):
        """Return the location of the image."""
        return self._coords

    @coords.setter
    def coords(self, value: tuple):
        self._coords = value

    @property
    def location(self):
        """Return the location of the image."""
        return self._location

    @location.setter
    def location(self, value: tuple):
        self._location = value

    def _populate_image_metadata(self):
        """
        Populate the image metadata.
        """
        if self.extension() == '.HEIC':
            self.heic_to_pillow_format()

        self._populate_jpeg_metadata()

    def _populate_jpeg_metadata(self):
        try:
            image = PIL.Image.open(self.path)

            # Attempt to extract EXIF data
            exif_data = {}
            if hasattr(image, '_getexif'):  # Check if the image has EXIF data
                exif_info = image._getexif()
                if exif_info is not None:
                    for tag, value in exif_info.items():
                        decoded = TAGS.get(tag, tag)
                        exif_data[decoded] = value

            self.width = exif_data['ExifImageWidth'] if 'ExifImageWidth' in exif_data else image.width
            self.height = exif_data['ExifImageHeight'] if 'ExifImageHeight' in exif_data else image.height
            self.coords = self.convert_gps_data(exif_data['GPSInfo']) if 'GPSInfo' in exif_data else None
            self.location = self.get_location_by_country() if self.coords else None
        except Exception as e:
            print(f"Failed to extract metadata from {self.path}. Error: {e}")

    def populate_heic_metadata(self):
        pass

    def heic_to_pillow_format(self):
        """
        Creates jpeg version of HEIC file in order to extract metadata using pillow library

        params:
        - heic_path: Path to the HEIC file.
        """
        try:
            subprocess.run(['heif-convert', self.path, self.path.split('.')[0]+'.jpeg'], check=True)
            self.path = self.path.split('.')[0]+'.jpeg'
        except subprocess.CalledProcessError as e:
            print(f"Failed to convert {self.path} to JPEG. Error: {e}")

    def get_location_by_country(self):
        """
        Get the location of the image by country using proximity logic.

        Parameters:
        - latitude: The latitude of the image.
        - longitude: The longitude of the image.

        Returns:
        The country of the image.
        """
        latitude, longitude = self.coords

        # Load the countries data
        countries = pd.read_csv('../../country-coord.csv')

        # Apply the Haversine formula to each country's coordinates
        countries['Distance'] = countries.apply(
            lambda row: Image.haversine(latitude, longitude, row['Latitude (average)'],
                                                 row['Longitude (average)']), axis=1)

        # Find the country with the minimum distance to the given coordinates
        nearest_country = countries.loc[countries['Distance'].idxmin()]

        if not nearest_country.empty:
            return nearest_country['Country']
        else:
            return "No country found for these coordinates."

    @staticmethod
    def dms_to_decimal(degrees, minutes, seconds, direction):
        """
        Converts degrees, minutes, and seconds to decimal degrees.

        Parameters:
        - degrees, minutes, seconds: The parts of the DMS value.
        - direction: The compass direction ('N', 'S', 'E', 'W').

        Returns:
        The decimal degree representation.
        """
        decimal = degrees + (minutes / 60.0) + (seconds / 3600.0)
        if direction in ['S', 'W']:
            decimal = -decimal
        return decimal

    @staticmethod
    def convert_gps_data(gps_data: dict) -> tuple:
        """
        Converts GPS data from EXIF format to readable latitude and longitude.

        Parameters:
        - gps_data: A dictionary containing GPS data in EXIF format.

        Returns:
        A tuple containing (latitude, longitude) in decimal degrees.
        """
        latitude_dms = gps_data.get(2)
        latitude_direction = gps_data.get(1)
        longitude_dms = gps_data.get(4)
        longitude_direction = gps_data.get(3)

        if latitude_dms and latitude_direction and longitude_dms and longitude_direction:
            latitude = Image.dms_to_decimal(latitude_dms[0], latitude_dms[1], latitude_dms[2], latitude_direction)
            longitude = Image.dms_to_decimal(longitude_dms[0], longitude_dms[1], longitude_dms[2], longitude_direction)
            return latitude, longitude
        else:
            return None

    @staticmethod
    def haversine(lat1, lon1, lat2, lon2):
        """
        Calculate the great circle distance in kilometers between two points
        on the earth (specified in decimal degrees).
        """
        # Convert decimal degrees to radians
        lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])

        # Haversine formula
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = np.sin(dlat / 2) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2) ** 2
        c = 2 * np.arcsin(np.sqrt(a))
        r = 6371  # Radius of earth in kilometers
        return c * r


if __name__ == "__main__":
    #ca = FileSystemCache()
    #file = Image("/Users/yachitrasivakumar/Desktop/location/IMG_5619.HEIC", ca)
    #print(file.width, file.height, file.coords, file.location)
    pass


