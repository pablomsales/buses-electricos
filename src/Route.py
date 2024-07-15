import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import Section


class Route:

    def __init__(self, filepath):
        if filepath:
            self._data = self._load_data(filepath)
            self.sections = self._process_sections(self._data)

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

        # lowercase headers
        df.columns = map(str.lower, df.columns)

        # if 2 first rows took data at 0.00s, remove first row
        if df.iloc[1, 0] == 0:
            df = df.drop([0])

        return df

    def _process_sections(self, df):
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
            start_time = start_section[1]
            end_time = end_section[1]
            timestamps = (start_time, end_time)

            # obtain speed
            start_speed = start_section[6]
            end_speed = end_section[6]
            speeds = (start_speed, end_speed)

            # obtain coordinates (Lat, Long, Alt)
            start_coord = (start_section[2], start_section[3], start_section[4])
            end_coord = (end_section[2], end_section[3], end_section[4])
            coordinates = (start_coord, end_coord)

            # create Section object and append to the rest of sections
            section = Section(coordinates, speeds, timestamps)
            sections.append(section)

        return sections

    def plot(self):
        """
        Plots the route in 3D using matplotlib
        """
        pass
