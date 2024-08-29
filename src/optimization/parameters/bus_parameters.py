import json

from parameter import Parameter


class BusParameters:

    def __init__(self, params_path):
        self.parameters = self._load_parameters(params_path)

        self.bus_mass = Parameter(**self.parameters["bus_mass"])
        self.engine_power = Parameter(**self.parameters["engine_power"])
        self.battery_capacity = Parameter(**self.parameters["battery"]["capacity"])
        self.battery_mass = Parameter(**self.parameters["battery"]["mass"])
        self.time_between_charges = Parameter(
            **self.parameters["battery"]["time_between_charges"]
        )

    def _load_parameters(path):
        # Open the JSON file and load its content
        try:
            with open(path, "r") as file:
                data = json.load(file)
                return data["parameters"]

        except FileNotFoundError:
            print(f"Error: The file {path} was not found.")
            return None

        except json.JSONDecodeError:
            print(f"Error: The file {path} is not a valid JSON file.")
            return None
