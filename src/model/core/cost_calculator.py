class CostCalculator:
    """
    Clase para calcular los costos asociados al autobús eléctrico, como el costo de la batería
    y el costo del consumo de electricidad.

    Parameters
    ----------
    bus : Bus
        Instancia de la clase Bus que representa el autobús eléctrico.
    electricity_cost : float
        Costo de la electricidad por kWh (€).
    battery_capacity_cost : float
        Costo de la capacidad de la batería por kWh (€).
    """

    def __init__(self, bus, electricity_cost: float, battery_capacity_cost: float):
        self.bus = bus
        self.electricity_cost = electricity_cost  # €/kWh
        self.battery_capacity_cost = battery_capacity_cost  # €/kWh

    def calculate_costs(self, consumption: float):
        """
        Calcula los costos totales del autobús eléctrico, incluyendo el costo del autobús
        y el costo del consumo eléctrico.

        Parameters
        ----------
        consumption : float
            Consumo total de electricidad en kWh.

        Returns
        -------
        tuple of (float, float)
            - El costo del autobús, redondeado a dos decimales.
            - El costo del consumo eléctrico, redondeado a dos decimales.
        """
        bus_cost = self._get_bus_cost()
        consumption_cost = self._get_consumption_cost(consumption)
        return float(round(bus_cost, 2)), float(round(consumption_cost, 2))

    def _get_bus_cost(self):
        """
        Calcula el costo total del autobús, incluyendo el costo base y el costo de la
        batería en función de su capacidad.
        """
        base_cost = 450000
        battery_capacity_kWh = self.bus.get_battery_capacity_kWh()
        battery_cost = battery_capacity_kWh * self.battery_capacity_cost
        return base_cost + battery_cost

    def _get_consumption_cost(self, consumption: float):
        """
        Calcula el costo total del consumo eléctrico basado en el consumo de kWh.
        """
        return consumption * self.electricity_cost
