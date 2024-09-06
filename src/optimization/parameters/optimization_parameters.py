from bus_parameters import BusParameters
from charging_points import ChargingPoints


class OptimizationParameters:

    def __init__(self, bus_parameters_path, charging_points_path):
        self.bus_parameters = BusParameters(bus_parameters_path)
        self.charging_points = ChargingPoints(charging_points_path)

    def get_parameters(self):
        return [
            *self.bus_parameters.get_parameters(),
            *self.charging_points.get_parameters(),
        ]
