from core.bus.engine.base_engine import BaseEngine


class ElectricalEngine(BaseEngine):
    """
    ElectricalEngine class represents an electric engine.
    """

    def __init__(self, max_power, efficiency, battery):
        super().__init__(max_power, efficiency)
        self.battery = battery

    @property
    def battery_depth_of_discharge(self):
        return self.battery.depth_of_discharge

    def consumption(self, power, time, km=None):
        """
        Calculate electric consumption in Wh.
        """
        power = self._adjust_power(power)
        hours = time / 3600  # convert seconds to hours

        # Compute consumption in Wh and Ah
        watts_hour = power * hours
        ampers_hour = watts_hour / self.battery.voltage_v

        if ampers_hour < 0:
            self.battery.charge(ampers_hour)
        else:
            self.battery.discharge(ampers_hour, time)

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

    def get_battery_depth_of_discharge(self):
        return self.battery.depth_of_discharge

    def __str__(self):
        return "Engine Type: Electric\n" + super().__str__()
