from core.bus.bus import Bus
from core.bus.engine.battery import Battery
from core.bus.engine.electrical_engine import ElectricalEngine
from core.bus.engine.fuel_engine import FuelEngine
from core.bus.fuel import Fuel
from core.route.emissions import Emissions


class Config:
    def __init__(self, electric, euro_standard="EURO_6"):
        """
        Class to create the configuration of the bus and emissions.

        Parameters
        ----------
        electric : bool, optional
            If the bus is electric, by default True
        euro_standard : str, optional
            The EURO standard of the bus, by default "EURO_6"
        """
        self.electric = electric
        self.euro_standard = euro_standard

    def create_bus(self):
        """
        Create a bus instance with the engine and fuel selected.

        Returns
        -------
        Bus
            The bus instance created
        """
        if self.electric:
            # Create an electric bus instance
            bus_instance = self._create_electric_bus()

        else:
            # Create a fuel bus instance
            bus_instance = self._create_fuel_bus()

        return bus_instance

    def _create_electric_bus(self):
        """
        Create an electric bus instance with the battery and electrical engine selected.

        Returns
        -------
        Bus
            The bus instance created
        """
        # Create a battery instance
        battery_instance = Battery(
            initial_capacity_ah=1225,
            voltage_v=400,
            max_cycles=3000,  # parametro estatico para datathon
            initial_soc_percent=100,  # parametro estatico para datathon
            min_state_of_health=80,  # parametro estatico para datathon
        )

        # Create an electrical engine instance
        engine_instance = ElectricalEngine(
            max_power=240,
            efficiency=92,  # parametro estatico para datathon
            battery=battery_instance,
        )

        # Create a bus instance
        bus_instance = Bus(
            mass=20000,
            drag_coefficient=0.8,  # parametro estatico para datathon
            frontal_area=9.0,  # parametro estatico para datathon
            rolling_resistance_coefficient=0.01,  # parametro estatico para datathon
            engine=engine_instance,
        )

        return bus_instance

    def _create_fuel_bus(self):
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
            max_power=200000,
            efficiency=0.35,  # 0 a 1
        )

        # Create a bus instance
        bus_instance = Bus(
            mass=20000,
            drag_coefficient=0.8,
            frontal_area=9.0,
            rolling_resistance_coefficient=0.01,
            engine=engine_instance,
        )

        return bus_instance

    def create_emissions(self):
        """
        Create an emissions instance with the EURO standard selected.

        Returns
        -------
        Emissions
            The emissions instance created
        """
        # Crear una instancia de Emissions con el estándar EURO deseado
        emissions_instance = Emissions(
            euro_standard=self.euro_standard,
            electric=self.electric,
        )
        return emissions_instance
