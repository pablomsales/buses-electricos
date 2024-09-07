from core.bus.engine.base_engine import BaseEngine


class ElectricalEngine(BaseEngine):
    """
    ElectricalEngine class represents an electric engine.
    """

    def __init__(self, max_power, efficiency, battery):
        super().__init__(max_power, efficiency)
        self.battery = battery
        self.electric = True

    @property
    def battery_state_of_health(self):
        return self.battery.state_of_health

    def consumption(self, power, time, km=None):
        """
        Calculate electric consumption in Wh.
        """
        power = self._adjust_power(power)
        hours = time / 3600  # convert seconds to hours

        # Compute consumption in Wh and Ah
        watts_hour = power * hours
        ampers_hour = watts_hour / self.battery.voltage_v

        self.battery.update_soc_and_degradation(ampers_hour, time)

        return {
            "Wh": watts_hour,
            "Ah": ampers_hour,
            "L/h": 0,  # 0 for ElectricalEngine
            "L/km": 0,  # "" "" ""
        }

    def get_battery_state_of_charge(self):
        return self.battery.state_of_charge_percent

    def get_battery_degradation_in_section(self):
        return self.battery.degradation_in_section

    def get_battery_state_of_health(self):
        return self.battery.state_of_health

    def get_battery_capacity_kWh(self):
        return self.battery.initial_capacity_kWh

    def get_total_time_below_min_soc(self):
        return self.battery.total_time_below_min_soc

    def __str__(self):
        return "Engine Type: Electric\n" + super().__str__()
