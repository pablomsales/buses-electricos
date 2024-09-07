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
        if self.bus.engine.electric:
            self.cost_calculator = self._config.cost_calculator

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

    def run(self, n_days: int = 1):
        """
        Run the simulation.

        Args:
            n_days (int): Number of days you want to simulate, default is 1. One day has 16 iterations (routes).

        Returns:
            A dictionary with the results of the simulation.
        """
        if self.bus.engine.electric:
            self._run_electric(n_iters=n_days * 16)
        else:
            self._run_combustion(n_iters=n_days * 16)

    def _run_electric(self, n_iters):
        power = self._get_param_by_charging_point_id(
            f"{self.charging_point_id}", "power_watts"
        )

        distance_of_charging_point = self._get_param_by_charging_point_id(
            f"{self.charging_point_id}", "distance_km"
        )

        # Inicializar tiempo
        time_to_charging_point_s = self._get_param_by_charging_point_id(
            f"{self.charging_point_id}", "time_min"
        )
        time_to_charging_point_s *= 60  # convertimos a segundos

        route_length_km = self.route.length_km

        # Calcular el factor para ajustar el consumo y las emisiones
        factor = (route_length_km + distance_of_charging_point) / route_length_km

        # Inicializar número de buses en la ruta
        n_buses = 1

        # Inicializar el tiempo de conducción
        availability_time_s = 0.0

        # Inicializar acumuladores para consumo, emisiones y degradación de batería
        consumption = 0.0
        emissions = {"NOx": 0.0, "CO": 0.0, "HC": 0.0, "PM": 0.0, "CO2": 0.0}
        battery_degradation = 0.0
        unavailability_time_s = 0.0

        for _ in tqdm(range(n_iters)):
            if self.soc() < self.min_battery_charge:
                # Carga la batería en el punto de carga
                charging_time_s = self.bus.engine.battery.charge_in_charging_point(
                    power=power, desired_soc=self.max_battery_charge
                )
                # agregamos tiempo de inoperabilidad del bus agregando el tiempo de carga
                # y el tiempo de ida y vuelta al punto de carga (por eso t * 2)
                unavailability_time_s += charging_time_s + 2 * time_to_charging_point_s
                # añadimos un bus a la ruta
                n_buses = 2

            # Actualizamos número de pasajeros manualmente
            self.bus.update_num_travellers()

            # Obtener valores acumulados de consumo y emisiones por sección
            new_consumption, *new_emissions, new_battery_degradation = (
                self._cumulative_consumption_and_emissions_electric()
            )

            # Ajustar los valores usando el factor calculado
            new_consumption *= factor
            new_emissions = [emission * factor for emission in new_emissions]
            new_battery_degradation *= factor

            # Acumular los valores
            consumption += new_consumption
            battery_degradation += new_battery_degradation

            # Acumular emisiones individuales para cada contaminante
            emissions_keys = ["NOx", "CO", "HC", "PM", "CO2"]
            for key, emission in zip(emissions_keys, new_emissions):
                emissions[key] += emission

            # Actualizar el tiempo de disponibilidad
            availability_time_s += self.route.duration_time

        # Configurar el tiempo final de disponibilidad
        availability_time_s -= unavailability_time_s

        bus_cost, consumption_cost = self.cost_calculator.calculate_costs(consumption)
        total_time_below_min_soc = self.bus.get_total_time_below_min_soc()

        # Guardar los resultados finales en un archivo CSV
        with open(
            os.path.join("simulation_results", "electric_simulation_results.csv"),
            mode="w",
            newline="",
        ) as file:
            writer = csv.writer(file)
            writer.writerow(
                [
                    "consumption_Wh",
                    "NOx_g",
                    "CO_g",
                    "HC_g",
                    "PM_g",
                    "CO2_g",
                    "battery_degradation_%",
                    "bus_cost",
                    "consumption_cost",
                    "availability_time_s",
                    "unavailability_time_s",
                    "n_buses",
                    "total_time_below_min_soc",
                ]
            )
            writer.writerow(
                [
                    consumption,
                    emissions["NOx"],
                    emissions["CO"],
                    emissions["HC"],
                    emissions["PM"],
                    emissions["CO2"],
                    battery_degradation,
                    bus_cost,
                    consumption_cost,
                    availability_time_s,
                    unavailability_time_s,
                    n_buses,
                    total_time_below_min_soc,
                ]
            )

        return {
            "consumption": consumption,
            "NOx": emissions["NOx"],
            "CO": emissions["CO"],
            "HC": emissions["HC"],
            "PM": emissions["PM"],
            "CO2": emissions["CO2"],
            "battery_degradation": battery_degradation,
            "bus_cost": bus_cost,
            "consumption_cost": consumption_cost,
            "availability_time_s": availability_time_s,
            "unavailability_time_s": unavailability_time_s,
            "n_buses": n_buses,
            "total_time_below_min_soc": total_time_below_min_soc,
        }

    def _run_combustion(self, n_iters):
        # Inicializar acumuladores para consumo y emisiones
        consumption = 0.0
        emissions = {"NOx": 0.0, "CO": 0.0, "HC": 0.0, "PM": 0.0, "CO2": 0.0}

        for _ in tqdm(range(n_iters)):
            # Actualizamos número de pasajeros manualmente
            self.bus.update_num_travellers()

            # Obtener valores acumulados de consumo y emisiones por sección
            new_consumption, *new_emissions = (
                self._cumulative_consumption_and_emissions_combustion()
            )

            # Acumular los valores
            consumption += new_consumption

            # Acumular emisiones individuales para cada contaminante
            emissions_keys = ["NOx", "CO", "HC", "PM", "CO2"]
            for key, emission in zip(emissions_keys, new_emissions):
                emissions[key] += emission

        # Guardar los resultados finales en un archivo CSV
        with open(
            os.path.join("simulation_results", "combustion_simulation_results.csv"),
            mode="w",
            newline="",
        ) as file:
            writer = csv.writer(file)
            writer.writerow(
                [
                    "consumption_L",
                    "NOx_g",
                    "CO_g",
                    "HC_g",
                    "PM_g",
                    "CO2_g",
                ]
            )
            writer.writerow(
                [
                    consumption,
                    emissions["NOx"],
                    emissions["CO"],
                    emissions["HC"],
                    emissions["PM"],
                    emissions["CO2"],
                ]
            )

        return {
            "consumption": consumption,
            "NOx": emissions["NOx"],
            "CO": emissions["CO"],
            "HC": emissions["HC"],
            "PM": emissions["PM"],
            "CO2": emissions["CO2"],
        }

    def _cumulative_consumption_and_emissions_electric(self):
        """
        Calculate and accumulate consumption and emissions data across all sections.

        Returns:
            A list with accumulated values for consumption in Wh, emissions (NOx, CO, HC, PM, CO2) in grams,
            and battery degradation.
        """
        # Inicializar acumuladores para los valores deseados
        total_wh = 0.0
        total_battery_degradation = 0.0
        # Inicializar un diccionario para acumular cada contaminante por separado
        total_emissions = {"NOx": 0.0, "CO": 0.0, "HC": 0.0, "PM": 0.0, "CO2": 0.0}

        # Iterar a través de las secciones de la ruta y acumular los datos necesarios
        for sect in self.route.sections:
            # Extraer los valores de emisiones y consumo
            sect_emissions = {
                key: float(value) for key, value in sect.section_emissions.items()
            }
            sect_consumption = [float(value) for value in sect.consumption.values()]

            # Duración de la sección en segundos
            duration = sect.end_time - sect.start_time

            # Acumular Wh y degradación de batería
            total_wh += sect_consumption[0]  # "Wh"
            total_battery_degradation += (
                sect.get_battery_degradation_in_section()
            )  # "battery_degradation" in 0-1

            # Acumular las emisiones de cada contaminante multiplicadas por la duración
            for contaminant, emission in total_emissions.items():
                if contaminant in sect_emissions:
                    total_emissions[contaminant] += (
                        sect_emissions[contaminant] * duration
                    )

        # Crear la lista de retorno con los valores acumulados
        result = (
            [total_wh] + list(total_emissions.values()) + [total_battery_degradation]
        )

        return result

    def _cumulative_consumption_and_emissions_combustion(self):
        """
        Calculate and accumulate consumption and emissions data across all sections.

        Returns:
            A list with accumulated values for consumption in Wh, emissions (NOx, CO, HC, PM, CO2) in grams,
            and battery degradation.
        """
        # Inicializar acumuladores para los valores deseados
        total_L = 0.0
        # Inicializar un diccionario para acumular cada contaminante por separado
        total_emissions = {"NOx": 0.0, "CO": 0.0, "HC": 0.0, "PM": 0.0, "CO2": 0.0}

        # Iterar a través de las secciones de la ruta y acumular los datos necesarios
        for sect in self.route.sections:
            # Duración de la sección en segundos
            duration = sect.end_time - sect.start_time  # seconds
            # Extraer los valores de emisiones y consumo
            sect_emissions = {
                key: float(value) for key, value in sect.section_emissions.items()
            }
            sect_consumption = (
                float(sect.consumption["L/h"]) * duration
            ) / 3600  # "L/h" -> "L"

            # Acumular L
            total_L += sect_consumption  # "L"

            # Acumular las emisiones de cada contaminante multiplicadas por la duración
            for contaminant, emission in total_emissions.items():
                if contaminant in sect_emissions:
                    total_emissions[contaminant] += (
                        sect_emissions[contaminant] * duration
                    )

        # Crear la lista de retorno con los valores acumulados
        result = [total_L] + list(total_emissions.values())

        return result

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
