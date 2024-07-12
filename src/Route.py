import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import Section


class Route:

    def __init__(self, filepath):
        if filepath:
            self.data = self._load_data(filepath)
            self.sections = self._process_sections(self.data)

    @property
    def sections(self):
        return self.sections

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
        # procesar los datos por pares, es decir, iterar por el DataFrame
        # de tal modo que se cree un objeto de tipo Section() con la fila
        # que se esta manejando y la siguiente. Recordar manejar el caso
        # de la ultima fila para que no cree una Section sin final.

        for i, row in df.iloc[1, :].iterrows():
            # crear objeto Section() tal que:
            #   - inicio_Section: df[i, :]
            #   - fin_Section: df[i+1, :]
            pass

    def plot(self):
        """
        Plots the route in 3D using matplotlib
        """
        pass
