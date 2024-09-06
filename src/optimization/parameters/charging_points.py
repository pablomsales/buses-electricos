import json


class ChargingPoints:

    def __init__(self, path):
        self.charging_points = self._load_charging_points(path)

    def _load_charging_points(path): ...

    def get_charging_points(self) -> list: ...
