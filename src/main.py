import os

from optimization.algorithms.differential_evolution import DifferentialEvolution
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

    # Initialize Fitness Function
    # fitness_func = Fitness()
    fitness_func = ...

    # Run optimization
    optimizer = DifferentialEvolution()
    best_result = optimizer.optimize(fitness_func, opt_params)

    print(best_result)


if __name__ == "__main__":
    main()
