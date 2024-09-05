class BaseEngine:
    """
    BaseEngine class represents the base engine with common attributes and methods.
    """

    def __init__(self, max_power, efficiency):
        self._max_power = max_power * 1000  # in Watts
        self.efficiency = efficiency  # in range [0, 1]

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
        else:
            raise ValueError("Efficiency should be in the range (0, 1]")

    def _adjust_power(self, power):
        """
        Adjust power based on max power and efficiency.
        """
        if power <= self._max_power:
            return power * self._efficiency
        else:
            return self._max_power * self._efficiency

    def __str__(self):
        return (
            f"Engine Type: {self.type}\n"
            f"Max Power: {self.max_power} W\n"
            f"Efficiency: {self.efficiency * 100} %"
        )
