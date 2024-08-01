from fuel import Fuel


class Engine:
    """
    Engine class represents the engine of a vehicle. It can be either combustion or electric.
    """

    def __init__(self, engine_type, max_power, efficiency, fuel=None):
        self._engine_type = engine_type  # "combustion" or "electric"
        self._max_power = max_power  # in Watts
        self._efficiency = efficiency  # between 0 and 1
        if engine_type != "electric":
            if fuel:
                self._fuel = fuel  # Fuel instance
            else:
                raise ValueError("Fuel parameter expected for engine_type='combustion'")

    @property
    def engine_type(self):
        """
        Engine type object.
        """
        return self._engine_type

    @engine_type.setter
    def engine_type(self, value):
        if value in ["combustion", "electric"]:
            self._engine_type = value
        else:
            raise ValueError("Engine type must be either 'combustion' or 'electric'")

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

    @property
    def max_power(self):
        """
        Maximum power of the engine in Watts.
        """
        return self._max_power

    @max_power.setter
    def max_power(self, value):
        if value > 0:
            self._max_power = value

    @property
    def efficiency(self):
        """
        Efficiency of the engine in the range [0, 1].
        """
        return self._efficiency

    @efficiency.setter
    def efficiency(self, value):
        if 0 < value <= 1:
            self._efficiency = value

    def consumption(self, power, time, kilometers=None):
        """
        Calculate the overall energy or fuel consumption.
        """

        if self.engine_type == "electric":
            hours = time / 3600  # convert seconds to hours
            consumption = power * hours  # compute Wh

        else:  # (enginte_type == 'combustion')
            lhv = self.fuel.lhv  # obtain selected fuel PCI
            energy = (power * time) / self.efficiency  # compute amount of energy
            litres = energy / lhv  # obtain the spent litres of fuel

            if kilometers:
                consumption = litres / kilometers  # finally, compute L/km
            else:
                consumption = litres / time

        return consumption

    def __str__(self):
        return (
            f"Engine Type: {self.type}\n"
            f"Max Power: {self.max_power} W\n"
            f"Efficiency: {self.efficiency * 100} %"
        )
