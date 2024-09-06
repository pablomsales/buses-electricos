import numpy as np
from core.bus.engine.base_engine import BaseEngine


class Bus:
    """
    Class to represent a bus.
    """

    def __init__(
        self,
        bus_mass,
        drag_coefficient,
        frontal_area,
        rolling_resistance_coefficient,
        engine,
    ):
        """
        Initialize a Bus instance.

        Parameters
        ----------
        mass : float
            Mass of the bus in kg.
        drag_coefficient : float
            Drag coefficient of the bus.
        frontal_area : float
            Frontal area of the bus in m².
        rolling_resistance_coefficient : float
            Rolling resistance coefficient of the bus.
        engine : BaseEngine
            Engine object representing the bus engine.
        """
        self.num_travellers = self.update_num_travellers()
        self.bus_mass = bus_mass
        self._drag_coefficient = drag_coefficient
        self._frontal_area = frontal_area
        self._rolling_resistance_coefficient = rolling_resistance_coefficient
        self.engine = engine

    @property
    def total_mass(self):
        """
        Total mass of the bus in kg
        """
        return self.bus_mass + (self.num_travellers * 70)

    @property
    def bus_mass(self):
        return self._bus_mass

    @bus_mass.setter
    def bus_mass(self, value):
        if value > 0:
            self._bus_mass = value

    @property
    def drag_coefficient(self):
        """
        Drag coefficient of the bus
        """
        return self._drag_coefficient

    @drag_coefficient.setter
    def drag_coefficient(self, value):
        if 0 < value < 1:  # typical values for drag coefficient
            self._drag_coefficient = value

    @property
    def frontal_area(self):
        """
        Frontal area of the bus in m²
        """
        return self._frontal_area

    @frontal_area.setter
    def frontal_area(self, value):
        if value > 0:
            self._frontal_area = value

    @property
    def rolling_resistance_coefficient(self):
        """
        Rolling resistance coefficient of the bus
        """
        return self._rolling_resistance_coefficient

    @rolling_resistance_coefficient.setter
    def rolling_resistance_coefficient(self, value):
        if value > 0:
            self._rolling_resistance_coefficient = value

    @property
    def engine(self):
        """
        Engine object representing the bus engine
        """
        return self._engine

    @engine.setter
    def engine(self, value):
        if isinstance(value, BaseEngine):
            self._engine = value
        else:
            print(type(value))
            raise ValueError(
                "Engine must be an instance of BaseEngine or its subclasses"
            )

    @staticmethod
    def update_num_travellers():
        # Set seed
        np.random.seed(16)
        # Generate num of travellers
        num_travellers = np.random.normal(loc=40, scale=30)
        # Clipping to stablished bounds and rounding to int
        return round(np.clip(num_travellers, 0, 146))

    def get_battery_state_of_charge(self):
        return self.engine.get_battery_state_of_charge()

    def get_battery_degradation_in_section(self):
        return self.engine.get_battery_degradation_in_section()

    def get_battery_state_of_health(self):
        return self.engine.get_battery_state_of_health()

    def get_battery_capacity_kWh(self):
        return self.engine.get_battery_capacity_kWh()

    def __str__(self):
        return (
            f"Bus Characteristics:\n"
            f"Mass: {self.mass} kg\n"
            f"Drag Coefficient: {self.drag_coefficient}\n"
            f"Frontal Area: {self.frontal_area} m²\n"
            f"Rolling Resistance Coefficient: {self.rolling_resistance_coefficient}\n"
            f"{str(self.engine)}"
        )
