class Engine:
    def __init__(self, type, max_power, max_torque, efficiency):
        self._type = type  # "combustion" or "electric"
        self._max_power = max_power  # in Watts
        self._max_torque = max_torque  # in Newton meters
        self._efficiency = efficiency  # between 0 and 1

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, value):
        if value in ["combustion", "electric"]:
            self._type = value

    @property
    def max_power(self):
        return self._max_power

    @max_power.setter
    def max_power(self, value):
        if value > 0:
            self._max_power = value

    @property
    def max_torque(self):
        return self._max_torque

    @max_torque.setter
    def max_torque(self, value):
        if value > 0:
            self._max_torque = value

    @property
    def efficiency(self):
        return self._efficiency

    @efficiency.setter
    def efficiency(self, value):
        if 0 < value <= 1:
            self._efficiency = value

    def power_output(self, required_power):
        """Calculate the actual power output considering the efficiency."""
        if required_power <= self._max_power:
            return required_power * self._efficiency
        else:
            return self._max_power * self._efficiency

    def torque_output(self, required_torque):
        """Calculate the actual torque output considering the efficiency."""
        if required_torque <= self._max_torque:
            return required_torque * self._efficiency
        else:
            return self._max_torque * self._efficiency

    def __str__(self):
        return (
            f"Engine Type: {self.type}\n"
            f"Max Power: {self.max_power} W\n"
            f"Max Torque: {self.max_torque} Nm\n"
            f"Efficiency: {self.efficiency * 100} %"
        )
