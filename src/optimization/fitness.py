import os

from model.core.model_config import ModelConfig
from src.model.core.model import Model


class Fitness:

    def __init__(self, weights: dict):
        self.weights = self._initialize_weights(weights)

    def _initialize_weights(self, weights):
        """
        Initialize the weights for the fitness function.
        """
        self._default_weights = {
            "consumption_weight": 1,
            "emissions_weight": 1,
            "battery_degradation_weight": 1,
        }
        if weights is None:
            return self._default_weights

        # Check all provided weight keys are expected
        self._validate_provided_weights(weights)

        # Combine default weights with provided weights
        # Use 0 for any missing keys
        combined_weights = {key: weights.get(key, 0) for key in self._default_weights}
        return combined_weights

    def _validate_provided_weights(self, weights):
        invalid_keys = [key for key in weights if key not in self._default_weights]
        if invalid_keys:
            raise ValueError(
                f"Invalid weight key(s): {', '.join(invalid_keys)}. Expected one of {', '.join(self._default_weights.keys())}."
            )

    def evaluate(self, parameters: list):

        # Unpack and process the parameters
        processed_params = self._process_parameters(parameters)

        # Run simulation model
        result = self._run_model_simulation(processed_params)

        # Calculate and return fitness value
        return self._get_fitness_value(result)

    def _process_parameters(self, parameters: list):
        """
        Process the list of parameters.
        """

        # unpack parameters list
        (
            bus_mass,
            engine_power,
            battery_capacity,
            battery_mass,
            time_between_charges,
            charging_point_id,
        ) = parameters

        # add masses and round charging_point_id to use it as int
        total_bus_mass = bus_mass + battery_mass
        charging_point_id = round(charging_point_id)

        return {
            "total_bus_mass": total_bus_mass,
            "engine_power": engine_power,
            "battery_capacity": battery_capacity,
            "time_between_charges": time_between_charges,
            "charging_point_id": charging_point_id,
        }

    def _run_model_simulation(self, params: dict):
        """
        Run the model simulation with the given parameters.
        """

        model_config = ModelConfig(
            electric=True,
            name="linea_d2_simulation_electric",
            filepath=os.path.join("data", "linea_d2", "linea_d2_simulation.csv"),
            mode="simulation",
            charging_point_id=params["charging_point_id"],
            initial_capacity_kWh=params["battery_capacity"],
            engine_max_power=params["engine_power"],
            bus_mass=params["total_bus_mass"],
            time_between_charges=params["time_between_charges"],
        )

        # Initialize and run the Model
        model = Model(config=model_config)
        return model.run(n_iters=1)

    def _get_fitness_value(self, result):
        """
        Calculate the fitness value based on the simulation result and the weights.
        """
        # Destructure the result for readability
        consumption = result["consumption"]
        emissions = result["emissions"]
        battery_degradation = result["battery_degradation"]

        # Calculate the fitness value
        fitness_value = (
            self.weights["consumption_weight"] * consumption
            + self.weights["emissions_weight"] * emissions
            + self.weights["battery_degradation_weight"] * battery_degradation
        )

        return fitness_value
