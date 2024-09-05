import csv
import os

import pandas as pd
from core.model_config import ModelConfig
from core.route.route import Route
from tqdm import tqdm


class Model:
    def __init__(self, config: ModelConfig):
        """
        Initialize a Model instance.

        Args:
            name (str): The name of the model.
            filepath (str): Path to the input data CSV file.
            bus: Instance of the Bus class.
            emissions: Instance of the Emissions class.
            simulation (bool): Whether the model is in simulation mode or not.
        """
        self._config = config
        self.name = self._config.name

        self._simulation = self._config.simulation
        self._data = self._load_data(self._config.filepath, self._simulation)
        self.bus = self._config.bus
        self.charging_point_id = self._config.charging_point_id
        self.min_battery_charge = self._config.min_battery_charge
        self.max_battery_charge = self._config.max_battery_charge
        self.route = Route(
            data=self._data,
            bus=self.bus,
            emissions=self._config.emissions,
            simulation=self._simulation,
        )

    def _load_data(self, filepath: str, simulation: bool) -> pd.DataFrame:
        """
        Load and process data from a CSV file based on if it is simulation data or real data.

        Returns
        --------
        pd.DataFrame: Processed data as a DataFrame.
        """
        df = pd.read_csv(filepath)

        if simulation:
            return self._process_simulation_data(df)
        else:
            return self._process_real_data(df)

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

    def run(self, n_iters: int = 16):

        power = self._get_param_by_charging_point_id(
            f"{self.charging_point_id}", "power_watts"
        )

        distance_of_charging_point = self._get_param_by_charging_point_id(
            f"{self.charging_point_id}", "distance_km"
        )

        route_length_km = self.route.length_km

        # Calcular el factor para ajustar el consumo y las emisiones
        factor = (route_length_km + distance_of_charging_point) / route_length_km

        consumption, emissions, battery_degradation = 0, 0, 0

        for _ in tqdm(range(n_iters)):
            if self.soc() < self.min_battery_charge:
                # Carga la batería en el punto de carga
                self.bus.engine.battery.charge_in_charging_point(
                    power=power, desired_soc=self.max_battery_charge
                )

                # Ajustar los valores usando el factor calculado
                new_consumption, new_emissions, new_battery_degradation = (
                    x * factor
                    for x in (new_consumption, new_emissions, new_battery_degradation)
                )

            new_consumption, new_emissions, new_battery_degradation = (
                self.cumulative_consumption_and_emissions()
            )
            consumption += new_consumption
            emissions += new_emissions
            battery_degradation += new_battery_degradation

        # print(f"Consumption: {round(consumption/1000)} kWh")
        # print(f"Emissions: {round(emissions)} grams")
        # print(f"Battery degradation: {round(battery_degradation, 6)}%")

    def cumulative_consumption_and_emissions(self):
        """
        Calculate and accumulate consumption and emissions data across all sections.

        Returns:
            A dictionary with accumulated values for consumption in Wh, emissions in grams, and battery degradation.
        """
        # Inicializar acumuladores para los valores deseados
        total_wh = 0.0
        total_emissions = 0.0
        total_battery_degradation = 0.0

        # Iterar a través de las secciones de la ruta y acumular los datos necesarios
        for sect in self.route.sections:
            # Extraer valores de consumo y emisiones
            sect_emissions = [float(value) for value in sect.section_emissions.values()]
            sect_consumption = [float(value) for value in sect.consumption.values()]

            # Duración de la sección en segundos
            duration = sect.end_time - sect.start_time

            # Acumular Wh y degradación de batería
            total_wh += sect_consumption[0]  # "Wh"
            total_battery_degradation += (
                sect.get_battery_degradation_in_section()
            )  # "battery_degradation" in 0-1

            # Acumular todas las emisiones en gramos
            total_emissions += sum(
                emission * duration for emission in sect_emissions
            )  # grams

        # Devolver una lista con los valores acumulados
        return [total_wh, total_emissions, total_battery_degradation]

    def soc(self):
        """
        Get the state of charge (SOC) of the battery.
        """
        return self.bus.engine.get_battery_state_of_charge()

    def _get_param_by_charging_point_id(self, charging_point_id: str, param: str):
        """
        Get a parameter value for a specific charging point.

        Args:
            charging_point_id (int): ID of the charging point.
            param (str): Name of the parameter to get.

        Returns:
            The value of the parameter.
        """
        return self.route.charging_points[charging_point_id][param]

    def consumption_and_emissions(self) -> None:
        """
        Calculate and save the consumption and emissions data to an output CSV file.
        """
        filename = os.path.join(self._config.output_dir, "output.csv")

        # Define headers based on engine type
        if self.bus.engine.electric:
            header = [
                "start",
                "end",
                "start_time",
                "end_time",
                "start_speed",
                "end_speed",
                "Wh",
                "Ah",
                "NOx",
                "CO",
                "HC",
                "PM",
                "CO2",
                "battery_degradation",
            ]
        else:
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

            if self.bus.engine.electric:
                row.append(sect.get_battery_degradation_in_section())

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
        return self.route.plot_combined_profiles(output_dir=self._config.output_dir)

    def plot_map(self):
        """
        Plot and save the map for the route.
        """
        return self.route.plot_map(output_dir=self._config.output_dir)
