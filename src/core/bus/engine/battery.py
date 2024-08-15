class Battery:

    def __init__(
        self, initial_capacity, max_num_cycles, soc, voltage, min_battery_health
    ):
        self._initial_capacity = initial_capacity  # in Ah (Ampers-hour)
        self.current_capacity = initial_capacity
        self._max_num_cycles = max_num_cycles
        self._completed_cycles = 0
        self.soc = soc  # State of Charge
        self._voltage = voltage
        self.min_battery_health = min_battery_health

    def charge(self, battery_input):
        # first get soc in Ah by multiplying by the current capacity of the battery
        soc_in_ampers_hour = self.current_capacity * (self.soc / 100)
        # add the input
        updated_soc_in_ampers_hour = soc_in_ampers_hour + battery_input
        # if the provided input exceeds the capacity, just get the current capacity
        soc_in_ampers_hour = min(updated_soc_in_ampers_hour, self.current_capacity)

        # NOTE: El codigo anterior descarta los Ah que no se usan. Sería mejor
        # "devolverselos" a la fuente de energia para que no sean energia perdida,
        # pero quiza no es tan importante para este modelado

        updated_soc = (soc_in_ampers_hour / self.current_capacity) * 100
        self.soc = updated_soc

    def discharge(self, battery_output):
        soc_in_ampers_hour = self.current_capacity * (self.soc / 100)
        # subtract the output
        updated_soc_in_ampers_hour = soc_in_ampers_hour - battery_output
        # if the substracted charge is more than the currently available
        if updated_soc_in_ampers_hour > 0:
            # get new state of charge
            updated_soc = (updated_soc_in_ampers_hour / self.current_capacity) * 100
            self._increase_completed_cycles(self.soc, updated_soc)
            self._update_current_capacity()
            # finally set new soc
            self.soc = updated_soc
        else:
            print("Batería agotada!!")

    def _increase_completed_cycles(self, initial_soc, final_soc):
        increase_value = (final_soc - initial_soc) / 100
        self._completed_cycles += increase_value

    def _update_current_capacity(self):
        pass
