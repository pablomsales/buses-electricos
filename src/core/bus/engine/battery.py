class Battery:

    def __init__(
        self,
        initial_capacity,
        max_num_cycles,
        state_of_charge,
        voltage,
        degradation_per_minute,
    ):
        self._initial_capacity = initial_capacity
        self._max_num_cycles = max_num_cycles
        self._completed_cycles = 0
        self.state_of_charge = state_of_charge
        self._voltage = voltage
        self._degradation_per_minute = degradation_per_minute

    @property
    def current_capacity(self):
        pass

    def charge_battery(self):
        pass

    def discharge_battery(self, time, consumption):
        pass
