import csv
import os

import pandas as pd

from core.route.route import Route


class Model:
    def __init__(self, name: str, filepath: str, bus, emissions, mode: str):
        """
        Initialize a Model instance.
        
        Args:
            name (str): The name of the model.
            filepath (str): Path to the input data CSV file.
            bus: Instance of the Bus class.
            emissions: Instance of the Emissions class.
            mode (str): Mode of operation, either 'real' or 'simulation'.
        """
        self.name = name
        self._validate_mode(mode)
        self._validate_filepath(filepath)
        self._output_dir = self._create_output_dir(name)

        self._mode = mode
        self._data = self._load_data(filepath, mode)
        self._bus = bus
        self.route = Route(
            data=self._data, bus=bus, emissions=emissions, mode=self._mode
        )

    def consumption_and_emissions(self) -> None:
        """
        Calculate and save the consumption and emissions data to an output CSV file.
        """
        filename = os.path.join(self._output_dir, "output.csv")

        if self._bus.engine.electric:
            # Prepare header and data rows for the electric engine
            header = [
                "start",
                "end",
                "start_time",
                "end_time",
                "start_speed",
                "end_speed",
                "Wh",
                "Ah",
                "L/h",
                "L/km",
                "NOx",
                "CO",
                "HC",
                "PM",
                "CO2",
                "battery_degradation",
            ]
            rows = []

            for sect in self.route.sections:
                sect_emissions = [float(value) for value in sect.section_emissions.values()]
                sect_consumption = [float(value) for value in sect.consumption.values()]

                row = [
                    sect.start,
                    sect.end,
                    sect.start_time,
                    sect.end_time,
                    sect.start_speed,
                    sect.end_speed,
                    *sect_consumption,
                    *sect_emissions,
                    sect.get_battery_degradation_in_section(),
                ]
                rows.append(row)
        
        else:
            # Prepare header and data rows for the combustion engine
            header = [
                "start",
                "end",
                "start_time",
                "end_time",
                "start_speed",
                "end_speed",
                "L/h",
                "L/km",
                "NOx",
                "CO",
                "HC",
                "PM",
                "CO2",
            ]
            rows = []

            for sect in self.route.sections:
                sect_emissions = [float(value) for value in sect.section_emissions.values()]
                sect_consumption = [float(value) for value in sect.consumption.values()]

                row = [
                    sect.start,
                    sect.end,
                    sect.start_time,
                    sect.end_time,
                    sect.start_speed,
                    sect.end_speed,
                    *sect_consumption,
                    *sect_emissions,
                ]
                rows.append(row)

        # Write to CSV file
        with open(filename, "w", newline="") as f:
            writer = csv.writer(f, delimiter=";")
            writer.writerow(header)
            writer.writerows(rows)

    def plot_combined_profiles(self):
        """
        Plot and save combined profiles for the route.
        """
        return self.route.plot_combined_profiles(output_dir=self._output_dir)

    def plot_map(self):
        """
        Plot and save the map for the route.
        """
        return self.route.plot_map(output_dir=self._output_dir)

    @staticmethod
    def _validate_mode(mode: str) -> None:
        if mode not in {"real", "simulation"}:
            raise ValueError("Expected parameter mode as 'real' or 'simulation'.")

    @staticmethod
    def _validate_filepath(filepath: str) -> None:
        if not filepath:
            raise ValueError(
                "No file path provided. Please provide a file path to load data."
            )
        if not filepath.endswith(".csv"):
            raise ValueError("Unsupported file format. Only .csv is supported.")

    def _load_data(self, filepath: str, mode: str) -> pd.DataFrame:
        """
        Load and process data from a CSV file based on the mode.

        Returns
        --------
        pd.DataFrame: Processed data as a DataFrame.
        """
        df = pd.read_csv(filepath)
        if mode == "real":
            return self._process_real_data(df)
        elif mode == "simulation":
            return self._process_simulation_data(df)

    @staticmethod
    def _process_real_data(df: pd.DataFrame) -> pd.DataFrame:
        """
        Process data to work in real mode, so it gets real values for speed & time
        """
        df = df.iloc[:, [2, 3, 4, 6, 8, 9]]
        df.columns = ["time", "latitude", "longitude", "altitude", "distance", "speed"]

        # Check and handle the first non-zero time entry
        if df.iloc[0]["time"] == 0:
            first_non_zero_index = df[df["time"] != 0].index[0]
            df = df.iloc[first_non_zero_index - 1 :]

        return df

    @staticmethod
    def _process_simulation_data(df: pd.DataFrame) -> pd.DataFrame:
        """
        Process data to work in simulation mode, e.g., setting up speed limits and other parameters.
        
        Returns:
        --------
        pd.DataFrame: Processed data as a DataFrame ready for simulation.
        """
        # Suponiendo que las columnas relevantes están presentes en el archivo CSV
        df.columns = ["latitude", "longitude", "altitude", "speed_limit"]
        
        return df

    def _create_output_dir(self, dir_name):
        final_path = os.path.join("outputs", dir_name)
        os.makedirs(final_path, exist_ok=True)
        return final_path
