from core.bus.engine.base_engine import BaseEngine


class Bus:
    """
    Class to represent a bus.
    """

    def __init__(
        self,
        mass,
        drag_coefficient,
        frontal_area,
        rolling_resistance_coefficient,
        engine,
    ):
        self._mass = mass
        self._drag_coefficient = drag_coefficient
        self._frontal_area = frontal_area
        self._rolling_resistance_coefficient = rolling_resistance_coefficient
        self.engine = engine  # Use the setter for validation

    @property
    def mass(self):
        """
        Mass of the bus in kg
        """
        return self._mass

    @mass.setter
    def mass(self, value):
        if value > 0:
            self._mass = value

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

    def get_battery_state_of_charge(self):
        return self.engine.get_battery_state_of_charge()

    def get_battery_degradation_in_section(self):
        return self.engine.get_battery_degradation_in_section()

    def get_battery_depth_of_discharge(self):
        return self.engine.get_battery_depth_of_discharge()

    def __str__(self):
        return (
            f"Bus Characteristics:\n"
            f"Mass: {self.mass} kg\n"
            f"Drag Coefficient: {self.drag_coefficient}\n"
            f"Frontal Area: {self.frontal_area} m²\n"
            f"Rolling Resistance Coefficient: {self.rolling_resistance_coefficient}\n"
            f"{str(self.engine)}"
        )
