import pandas as pd

from src.core.route import Route


class BaseModel:
    def __init__(self, filepath, bus, emissions):
        if filepath:
            self._data = self.__load_data(filepath)
        else:
            raise ValueError(
                "No file path provided. Please provide a file path to load data."
            )

        self.route = Route(data=self._data, bus=bus, emissions=emissions)

    @property
    def consumption(self):
        raise NotImplementedError("Subclasses should implement this method.")

    @property
    def emissions(self):
        raise NotImplementedError("Subclasses should implement this method.")

    def __load_data(self, filepath: str):
        """
        Load data from a file.
        """
        if filepath.endswith(".csv"):
            return self.__process_csv(filepath)
        else:
            raise ValueError("Unsupported file format. Only .csv is supported.")

    def __process_csv(self, filepath):
        """
        Process the CSV file.
        """
        # TODO: hay que ver como manejar esto para cuando se usa EstimatedModel
        df = pd.read_csv(filepath)
        df = df.iloc[:, [2, 3, 4, 6, 8, 9]]
        df.columns = ["time", "latitude", "longitude", "altitude", "distance", "speed"]
        if df.iloc[0]["time"] == 0:
            first_non_zero_index = df[df["time"] != 0].index[0]
            df = df.iloc[first_non_zero_index - 1 :]
        return df
