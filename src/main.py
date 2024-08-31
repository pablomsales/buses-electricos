import os

from scipy.optimize import differential_evolution

from optimization.fitness import Fitness
from optimization.parameters.optimization_parameters import OptimizationParameters


def main():

    # Define parameters paths
    bus_parameters = os.path.join("..", "data", "optimization_data", "bus.json")
    charging_points = os.path.join(
        "..", "data", "optimization_data", "charging_points.json"
    )

    # Initialize parameters
    opt_params = OptimizationParameters(
        bus_parameters=bus_parameters,
        charging_points=charging_points,
    )

    # get a list with the parameters bounds
    bounds = opt_params.get_parameters()

    # Initialize Fitness Function
    fitness_func = Fitness()

    # Run optimization
    best_result = differential_evolution(fitness_func.evaluate, bounds)

    print(best_result)


if __name__ == "__main__":
    main()
