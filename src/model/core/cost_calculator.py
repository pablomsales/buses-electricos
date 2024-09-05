import csv
import os


class CostCalculator:
    def __init__(self, bus, electricity_cost, battery_capacity_cost):
        self.bus = bus
        self.electricity_cost = electricity_cost  # €/kWh
        self.battery_capacity_cost = battery_capacity_cost  # €/kWh

    def total_cost(self):
        bus_cost = self._get_bus_cost()
        consumption_cost = self._get_consumption_cost()
        return round(bus_cost + consumption_cost, 2)

    def _get_bus_cost(self):
        base_cost = 450000
        battery_capacity_kWh = self.bus.get_battery_capacity_kWh()
        battery_cost = battery_capacity_kWh * self.battery_capacity_cost
        return base_cost + battery_cost

    def _get_consumption_cost(self):
        # Leer el archivo CSV y obtener el valor de consumo
        with open(os.path.join('simulation_results', 'simulation_results.csv'), mode="r") as file:
            reader = csv.reader(file)
            next(reader)  # Saltar la primera fila (encabezados)
            row = next(reader)  # Leer la única fila de datos
            consumo = float(
                row[0]
            )  # Obtener el valor de consumo y convertir a float si es necesario
        return consumo * self.electricity_cost
