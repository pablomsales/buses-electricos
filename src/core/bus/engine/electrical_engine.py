from core.bus.engine.base_engine import BaseEngine


class ElectricalEngine(BaseEngine):
    """
    ElectricalEngine class represents an electric engine.
    """

    def __init__(self, max_power, efficiency, battery):
        super().__init__(max_power, efficiency)
        self.battery = battery  # TODO: mirar si usar battery dentro de ElectricalEngine (creo que si)

    def consumption(self, power, time, km=None):
        """
        Calculate electric consumption in Wh.
        """
        power = self._adjust_power(power)
        hours = time / 3600  # convert seconds to hours
        consumption = power * hours

        return {"Wh": consumption, "L/h": 0, "L/km": 0}

    def __str__(self):
        return "Engine Type: Electric\n" + super().__str__()
