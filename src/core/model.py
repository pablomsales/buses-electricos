import pandas as pd

from src.core.route import Route


class Model:
    def __init__(self, filepath, bus, emissions, mode):
        self._validate_mode(mode)
        self._validate_filepath(filepath)

        self._mode = mode
        self._data = self._load_data(filepath)
        self.route = Route(data=self._data, bus=bus, emissions=emissions)

    @property
    def consumption(self):
        if self._mode == "real":
            return self.route.section.calculate_real_consumption()
        if self._mode == "estimation":
            return self.route.section.calculate_estimated_consumption()

    @property
    def emissions(self):
        if self._mode == "real":
            return self.route.section.calculate_real_emissions()
        if self._mode == "estimation":
            return self.route.section.calculate_estimated_emissions()

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
