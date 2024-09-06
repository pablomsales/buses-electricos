import os

import pandas as pd
from core.bus.bus import Bus
from core.bus.engine.battery import Battery
from core.bus.engine.electrical_engine import ElectricalEngine
from core.bus.engine.fuel_engine import FuelEngine
from core.bus.fuel import Fuel
from core.cost_calculator import CostCalculator
from core.route.emissions import Emissions


class ModelConfig:
    def __init__(
        self,
        electric: bool,
        name: str,
        filepath: str,
        simulation: bool,
        charging_point_id: int,
        min_battery_charge: float = 20,
        max_battery_charge: float = 80,
        initial_capacity_kWh=392,
        engine_max_power=240,  # kW
        bus_mass=20000,
        euro_standard="EURO_6",
    ):
        """
        Class to create the configuration of the bus and emissions.

        Parameters
        ----------
        electric : bool, optional
            If the bus is electric, by default True
        euro_standard : str, optional
            The EURO standard of the bus, by default "EURO_6"
        """
        self.name = name
        self._validate_filepath(filepath)
        self.filepath = filepath
        self.output_dir = self._create_output_dir(name)

        self.simulation = simulation
        self.electric = electric
        self.bus = self._create_bus(initial_capacity_kWh, engine_max_power, bus_mass)
        self.emissions = self._create_emissions(euro_standard)
        self.cost_calculator = CostCalculator(
            bus=self.bus,
            electricity_cost=0.15,  # €/kWh # valores estaticos en datahon, no tocar
            battery_capacity_cost=140,  # €/kWh # valores estaticos en datathon, no tocar
        )
        self.charging_point_id = charging_point_id
        self.min_battery_charge = min_battery_charge
        self.max_battery_charge = max_battery_charge

    @staticmethod
    def _validate_filepath(filepath: str) -> None:
        if not filepath:
            raise ValueError(
                "No file path provided. Please provide a file path to load data."
            )
        if not filepath.endswith(".csv"):
            raise ValueError("Unsupported file format. Only .csv is supported.")

    def _create_output_dir(self, dir_name):
        final_path = os.path.join("outputs", dir_name)
        os.makedirs(final_path, exist_ok=True)
        return final_path

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

    def _create_bus(self, initial_capacity_kWh, max_power, bus_mass):
        if self.electric:
            return self._create_electric_bus(initial_capacity_kWh, max_power, bus_mass)
        else:
            return self._create_fuel_bus(max_power, bus_mass)

    def _create_electric_bus(self, initial_capacity_kWh, max_power, bus_mass):
        """
        Create an electric bus instance with the battery and electrical engine selected.

        Returns
        -------
        Bus
            The bus instance created
        """
        # Create a battery instance
        battery_instance = Battery(
            initial_capacity_kWh=initial_capacity_kWh,
            voltage_v=400,  # parametro estatico para datathon
            max_cycles=3000,  # parametro estatico para datathon
            initial_soc_percent=100,  # parametro estatico para datathon
            min_state_of_health=80,  # parametro estatico para datathon
        )

        # Create an electrical engine instance
        engine_instance = ElectricalEngine(
            max_power=max_power,
            efficiency=0.92,  # parametro estatico para datathon (0 a 1)
            battery=battery_instance,
        )

        # Create a bus instance
        bus_instance = Bus(
            bus_mass=bus_mass,
            drag_coefficient=0.8,  # parametro estatico para datathon
            frontal_area=9.0,  # parametro estatico para datathon
            rolling_resistance_coefficient=0.01,  # parametro estatico para datathon
            engine=engine_instance,
        )

        return bus_instance

    def _create_fuel_bus(self, max_power, bus_mass):
        """
        Create a fuel bus instance with the fuel engine selected.

        Returns
        -------
        Bus
            The bus instance created
        """
        # Create a fuel instance
        fuel_instance = Fuel(fuel_type="diesel")

        # Create a fuel engine instance
        engine_instance = FuelEngine(
            fuel=fuel_instance,
            max_power=max_power,
            efficiency=0.35,  # 0 a 1
        )

        # Create a bus instance
        bus_instance = Bus(
            bus_mass=bus_mass,
            drag_coefficient=0.8,
            frontal_area=9.0,
            rolling_resistance_coefficient=0.01,
            engine=engine_instance,
        )

        return bus_instance

    def _create_emissions(self, euro_standard):
        return Emissions(euro_standard=euro_standard, electric=self.electric)
