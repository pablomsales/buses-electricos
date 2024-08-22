from core.bus.bus import Bus
from core.bus.engine.battery import Battery
from core.bus.engine.electrical_engine import ElectricalEngine
from core.bus.engine.fuel_engine import FuelEngine
from core.bus.fuel import Fuel
from core.route.emissions import Emissions

class Config:
    def __init__(self, electric=True, euro_standard="EURO_6"):
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
            # Crear instancia de Battery
            battery_instance = Battery(
                initial_capacity_ah=1225,
                voltage_v=400,
                max_cycles=3000,
                initial_soc_percent=100,
                min_state_of_health=80,
            )

            engine_instance = ElectricalEngine(
                max_power=240,
                efficiency=92,
                battery=battery_instance,
            )

        else:
            # Crear una instancia de Fuel
            fuel_instance = Fuel(fuel_type="diesel")

            # Crear una instancia de Engine con el fuel
            engine_instance = FuelEngine(
                fuel=fuel_instance,
                max_power=200,  # kW
                efficiency=0.35,  # 0 a 1
            )

        # Crear una instancia de Bus con el motor
        bus_instance = Bus(
            mass=18000,
            drag_coefficient=0.8,
            frontal_area=13.0,
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
        emissions_instance = Emissions(euro_standard=self.euro_standard)
        return emissions_instance
