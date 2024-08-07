import os

import pandas as pd

from core.route import Route


class Model:
    def __init__(self, name, filepath, bus, emissions, mode):
        self.name = name
        self._validate_mode(mode)
        self._validate_filepath(filepath)
        self._output_dir = self._create_output_dir(name)

        self._mode = mode
        self._data = self._load_data(filepath, mode)
        self.route = Route(
            data=self._data, bus=bus, emissions=emissions, mode=self._mode
        )

    @property
    def consumption_and_emissions(self):
        for section in self.route.sections:
            print(section)
        # sustituir lo de arriba para manejar el guardado en un csv de outputs

    def plot_combined_profiles(self):
        return self.route.plot_combined_profiles(output_dir=self._output_dir)

    def plot_map(self):
        return self.route.plot_map(output_dir=self._output_dir)

    @staticmethod
    def _validate_mode(mode):
        if mode not in {"real", "estimation"}:
            raise ValueError("Expected parameter mode as 'real' or 'estimation'.")

    @staticmethod
    def _validate_filepath(filepath):
        if not filepath:
            raise ValueError(
                "No file path provided. Please provide a file path to load data."
            )
        if not filepath.endswith(".csv"):
            raise ValueError("Unsupported file format. Only .csv is supported.")

    def _load_data(self, filepath: str, mode: str):
        """
        Load and process data from a CSV file based on the mode.
        """
        df = pd.read_csv(filepath)
        if mode == "real":
            return self._process_real_data(df)
        elif mode == "estimation":
            return self._process_estimation_data(df)

    @staticmethod
    def _process_real_data(df):
        df = df.iloc[:, [2, 3, 4, 6, 8, 9]]
        df.columns = ["time", "latitude", "longitude", "altitude", "distance", "speed"]

        # Check and handle the first non-zero time entry
        if df.iloc[0]["time"] == 0:
            first_non_zero_index = df[df["time"] != 0].index[0]
            df = df.iloc[first_non_zero_index - 1 :]

        return df

    @staticmethod
    def _process_estimation_data(df):
        # Add estimation logic here
        pass

    def _create_output_dir(self, dir_name):
        final_path = os.path.join("outputs", dir_name)
        os.makedirs(final_path, exist_ok=True)
        return final_path
