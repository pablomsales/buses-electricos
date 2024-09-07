class CostCalculator:
    def __init__(self, bus, electricity_cost, battery_capacity_cost):
        self.bus = bus
        self.electricity_cost = electricity_cost  # €/kWh
        self.battery_capacity_cost = battery_capacity_cost  # €/kWh

    def calculate_costs(self, consumption):
        bus_cost = self._get_bus_cost()
        consumption_cost = self._get_consumption_cost(consumption)
        return float(round(bus_cost, 2)), float(round(consumption_cost, 2))

    def _get_bus_cost(self):
        base_cost = 450000
        battery_capacity_kWh = self.bus.get_battery_capacity_kWh()
        battery_cost = battery_capacity_kWh * self.battery_capacity_cost
        return base_cost + battery_cost

    def _get_consumption_cost(self, consumption):
        return consumption * self.electricity_cost
