from core.bus.engine.base_engine import BaseEngine
from core.bus.fuel import Fuel


class FuelEngine(BaseEngine):
    """
    Represents a combustion engine.
    """

    def __init__(self, max_power, efficiency, fuel):
        """
        Initialize a FuelEngine with the maximum power, efficiency, and fuel.

        Args:
            max_power (float): The maximum power output of the engine in Watts.
            efficiency (float): The efficiency of the engine (0 to 1).
            fuel (Fuel): The fuel used by the engine.
        """
        super().__init__(max_power, efficiency)
        if not isinstance(fuel, Fuel):
            raise ValueError("fuel must be an instance of Fuel")
        self._fuel = fuel
        self.electric = False

    @property
    def fuel(self):
        """
        Fuel object representing the fuel used by the engine.
        """
        return self._fuel

    @fuel.setter
    def fuel(self, value):
        if isinstance(value, Fuel):
            self._fuel = value
        else:
            raise ValueError("fuel must be an instance of Fuel")

    def consumption(self, power, time, km) -> dict[str, float]:
        """
        Calculate fuel consumption.

        Args:
            power (float): The power demand in Watts.
            time (float): The time period over which the power is applied in seconds.
            km (float, optional): The distance covered in kilometers (if available).

        Returns:
            dict[str, float]: A dictionary containing:
                - "Wh": Always 0 for a combustion engine.
                - "L/h": Liters of fuel consumed per hour.
                - "L/km": Liters of fuel consumed per kilometer (if distance provided).
        """

        # If power is negative, consumption is zero.
        # NOTE: quizá no sea 0 y sea una constante
        if power < 0:
            return {
                "L/h": 0.0,
                "L/km": 0.0 if km is not None else None,
            }

        power = self._adjust_power(power)
        lhv = self.fuel.lhv  # Lower Heating Value of the fuel

        # Calculate the energy used
        energy = (power * time) / self._efficiency
        # Calculate fuel consumption in liters
        litres = energy / lhv

        consumption = {
            "L/h": litres / (time / 3600),  # Convert time from seconds to hours
            "L/km": litres / km if km is not None else None,
        }

        return consumption
