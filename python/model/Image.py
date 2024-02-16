from FileSystemNodeModel import File, FileSystemCache
import PIL.Image
from PIL.ExifTags import TAGS
import subprocess, pandas as pd
    

class Image(File):

    def __init__(self, path: str, cache):
        super().__init__(path, cache)
        self._width = None
        self._height = None
        self._coords = None
        self._location = None
        self._resolution = None
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

    @property
    def resolution(self):
        """Return the resolution of the image."""
        return self._resolution

    @resolution.setter
    def resolution(self, value):
        self._resolution = value

    def _populate_image_metadata(self):
        """
        Populate the image metadata.
        """
        if self.extension() == 'HEIC':
            self.heic_to_pillow_format()

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
            self.resolution = exif_data['XResolution'] if 'XResolution' in exif_data else None
            self.location = self.get_location_by_country(self.coords)

        except IOError:
            print(f"Error: Cannot open {self.path}")

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
    def get_location_by_country(latitude: float, longitude: float):
        """
        Get the location of the image by country.

        Parameters:
        - latitude: The latitude of the image.
        - longitude: The longitude of the image.

        Returns:
        The country of the image.
        """
        countries = pd.read_csv('/Users/yachitrasivakumar/Desktop/country-coord.csv')

        match = countries.loc[(countries['Latitude (average)'] == latitude) & (countries['Longitude (average)'] == longitude)]

        if not match.empty:
            return match.iloc[0]['Country']
        else:
            return "No country found for these coordinates."


if __name__ == "__main__":

    #testing
    #cache = FileSystemCache()
    #file_obj = Image('/Users/yachitrasivakumar/Downloads/IMG_5619.HEIC', cache)
    #print(file_obj.width, file_obj.height, file_obj.format, file_obj.location, file_obj.resolution)
    #file_obj = Image('/Users/yachitrasivakumar/Downloads/12382975864_2cd7755b03_b.jpg', {})
    #print(file_obj.width, file_obj.height, file_obj.format, file_obj.location, file_obj.resolution)
    #print(Image.get_location_by_country(53, -8))
    pass


