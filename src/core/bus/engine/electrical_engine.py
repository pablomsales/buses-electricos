from core.bus.engine.base_engine import BaseEngine


class ElectricalEngine(BaseEngine):
    """
    ElectricalEngine class represents an electric engine.
    """

    def __init__(self, max_power, efficiency, battery):
        super().__init__(max_power, efficiency)
        self.battery = battery  # TODO: mirar si usar battery dentro de ElectricalEngine

    def consumption(self, power, time, km=None):
        """
        Calculate electric consumption in Wh.
        """
        power = self._adjust_power(power)
        hours = time / 3600  # convert seconds to hours

        # Compute consumption in Wh and Ah
        watts_hour = power * hours
        ampers_hour = watts_hour / self.battery.voltage

        return {
            "Wh": watts_hour,
            "Ah": ampers_hour,
            "L/h": 0,  # 0 for ElectricalEngine
            "L/km": 0,  # "" "" ""
        }

    def __str__(self):
        return "Engine Type: Electric\n" + super().__str__()
