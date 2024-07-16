import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import Section


class Route:

    def __init__(self, filepath=None):
        if filepath:
            self._data = self._load_data(filepath)
            self.sections = self._process_sections(self._data)
        else:
            raise ValueError(
                "No file path provided. Please provide a file path to load data."
            )

    def _load_data(self, filepath: str):
        """
        Load data from a file.

        This method loads data from a file, processing it based on its format.
        It supports loading from .csv and .gpx files.

        Parameters:
        -----------
            filepath : str
            The path to the file to be loaded.

        Returns:
        --------
            The data loaded from the file, processed according to its format.

        Raises:
            ValueError: If the file format is not supported (.csv or .gpx).
        """

        if filepath.endswith(".csv"):
            data = self._process_csv(filepath)
        elif filepath.endswith(".gpx"):
            data = self._process_gpx(filepath)
        else:
            raise ValueError(
                "Unsupported file format. Only .csv and .gpx are supported."
            )

        return data

    def _process_csv(self, filepath):
        """
        Process CSV file data.

        Parameters
        ----------
        filepath : str
            The path to the CSV file.

        Returns
        -------
        pandas.DataFrame
            The processed data.
        """

        df = pd.read_csv(filepath)

        # select columns
        df = df.iloc[:, [2, 3, 4, 6, 8, 9]]

        # rename columns
        df.columns = ["time", "latitude", "longitude", "altitude", "distance", "speed"]

        # check if the first row's 'time' column is 0 and remove subsequent rows with 'time' = 0
        if df.iloc[0]["time"] == 0:
            # Find the first row where 'time' is not 0 after the first row
            first_non_zero_index = df[df["time"] != 0].index[0]
            # Keep all rows starting from the first row with 'time' not equal to 0
            df = df.iloc[first_non_zero_index - 1 :]

        return df

    def _process_sections(self, df: pd.DataFrame):
        """
        Groups the data in the corresponding road sections
        """
        sections = []
        # create one section for each two rows
        for i in range(df.shape[0] - 1):
            # select the two rows
            start_section = df.iloc[i, :]
            end_section = df.iloc[i + 1, :]

            # obtain timestamps
            start_time = start_section["time"]
            end_time = end_section["time"]
            timestamps = (start_time, end_time)

            # obtain speed
            start_speed = start_section["speed"]
            end_speed = end_section["speed"]
            speeds = (start_speed, end_speed)

            # obtain coordinates (Lat, Long, Alt)
            start_coord = (
                start_section["latitude"],
                start_section["longitude"],
                start_section["altitude"],
            )
            end_coord = (
                end_section["latitude"],
                end_section["longitude"],
                end_section["altitude"],
            )
            coordinates = (start_coord, end_coord)

            # create Section object and append to the rest of sections
            section = Section(coordinates, speeds, timestamps)
            ### APPEND DE UN OBJETO DE LA CLASE SECTION ??? ###
            sections.append(section)

        return sections

    def plot(self):
        """
        Plots the route in 3D using matplotlib
        """
        pass
