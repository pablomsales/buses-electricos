"""
Proyecto: Optimización de Rutas y Análisis de Sostenibilidad en Autobuses Eléctricos Urbanos

Autores:

- Chakhoyan Grigoryan, Razmik
  Correo: chakhoyanrazmik@gmail.com
  LinkedIn: https://www.linkedin.com/in/chakhoyanrazmik

- Menéndez Sales, Pablo
  Correo: pablomenendezsales@gmail.com
  LinkedIn: https://www.linkedin.com/in/pablo-m-sales

Fecha de creación: 12/07/2024
Última modificación: 09/09/2024
"""

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
        simulation: bool = True,  # NO CAMBIAR
        charging_point_id: int = 1,
        min_battery_charge: float = 20,
        max_battery_charge: float = 80,
        initial_capacity_kWh: float = 392,
        engine_max_power: float = 240,  # kW
        euro_standard: str = "EURO_6",  # NO CAMBIAR
    ):
        """
        Configuración para la simulación de un autobús y sus características.

        Parameters
        ----------
        electric : bool
            Indica si el autobús es eléctrico.
        name : str
            Nombre del modelo de autobús.
        filepath : str
            Ruta del archivo donde se almacenará la configuración y los resultados.
        simulation : bool
            Indica si se está realizando una simulación.
        charging_point_id : int, optional
            Identificador del punto de carga del autobús. Por defecto es 1.
        min_battery_charge : float, optional
            Carga mínima de la batería en porcentaje. Por defecto es 20.
        max_battery_charge : float, optional
            Carga máxima de la batería en porcentaje. Por defecto es 80.
        initial_capacity_kWh : float, optional
            Capacidad inicial de la batería en kWh. Por defecto es 392.
        engine_max_power : float, optional
            Potencia máxima del motor en kW. Por defecto es 240.
        euro_standard : str, optional
            Norma EURO del autobús. Por defecto es "EURO_6". NO CAMBIAR.

        Attributes
        ----------
        name : str
            Nombre del modelo de autobús.
        filepath : str
            Ruta del archivo para guardar la configuración y los resultados.
        simulation : bool
            Indica si se está realizando una simulación.
        electric : bool
            Indica si el autobús es eléctrico.
        bus : Bus
            Instancia de la clase Bus con la configuración inicial.
        emissions : Emissions
            Instancia de la clase Emissions basada en la norma EURO especificada.
        cost_calculator : CostCalculator, optional
            Instancia de la clase CostCalculator para calcular los costos asociados (solo si el autobús es eléctrico).
        charging_point_id : int
            Identificador del punto de carga del autobús.
        min_battery_charge : float
            Carga mínima de la batería en porcentaje.
        max_battery_charge : float
            Carga máxima de la batería en porcentaje.
        """
        self.name = name
        self._validate_filepath(filepath)
        self.filepath = filepath
        # self.output_dir = self._create_output_dir(name) # NO USAR DATATHON

        self.simulation = simulation
        self.electric = electric
        self.min_battery_charge = min_battery_charge
        self.max_battery_charge = max_battery_charge
        self.bus = self._create_bus(initial_capacity_kWh, engine_max_power)
        self.emissions = self._create_emissions(euro_standard)
        if self.electric:
            self.cost_calculator = CostCalculator(
                bus=self.bus,
                electricity_cost=0.15,  # €/kWh # valores estaticos en datahon, no tocar
                battery_capacity_cost=140,  # €/kWh # valores estaticos en datathon, no tocar
            )
        self.charging_point_id = charging_point_id

    @staticmethod
    def _validate_filepath(filepath: str) -> None:
        if not filepath:
            raise ValueError(
                "No file path provided. Please provide a file path to load data."
            )
        if not filepath.endswith(".csv"):
            raise ValueError("Unsupported file format. Only .csv is supported.")

    def _create_output_dir(self, dir_name: str) -> str:
        """
        Crea un directorio de salida para guardar los resultados.

        Parameters
        ----------
        dir_name : str
            Nombre del directorio que se creará dentro de la carpeta 'outputs'.

        Returns
        -------
        str
            Ruta completa del directorio creado.
        """
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

    def _create_bus(self, initial_capacity_kWh, max_power):
        """
        Crea una instancia de la clase Bus dependiendo de si el autobús es eléctrico o de combustible.

        Parameters
        ----------
        initial_capacity_kWh : float
            Capacidad inicial de la batería en kWh (solo se usa si el autobús es eléctrico).
        max_power : float
            Potencia máxima del motor en kW.

        Returns
        -------
        Bus
            Instancia de la clase Bus, ya sea eléctrica o de combustible.
        """
        if self.electric:
            return self._create_electric_bus(initial_capacity_kWh, max_power)
        else:
            return self._create_fuel_bus(max_power)

    def _create_electric_bus(self, initial_capacity_kWh, max_power):
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
            min_state_of_health=75,  # parametro estatico para datathon
            min_battery_charge=self.min_battery_charge,
        )

        # Create an electrical engine instance
        engine_instance = ElectricalEngine(
            max_power=max_power,  # parametro estatico para datathon
            efficiency=0.92,  # parametro estatico para datathon (0 a 1)
            battery=battery_instance,
        )

        # Create a bus instance
        bus_instance = Bus(
            bus_mass=15000,  # mas adelante se le agrega la masa de bateria
            drag_coefficient=0.8,  # parametro estatico para datathon
            frontal_area=9.0,  # parametro estatico para datathon
            rolling_resistance_coefficient=0.01,  # parametro estatico para datathon
            engine=engine_instance,
        )

        return bus_instance

    def _create_fuel_bus(self, max_power):
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
            bus_mass=18000,  # Mayor que en el eléctrico para una comparación justa
            drag_coefficient=0.8,
            frontal_area=9.0,
            rolling_resistance_coefficient=0.01,
            engine=engine_instance,
        )

        return bus_instance

    def _create_emissions(self, euro_standard):
        return Emissions(euro_standard=euro_standard, electric=self.electric)
