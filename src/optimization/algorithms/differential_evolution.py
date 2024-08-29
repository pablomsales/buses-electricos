from optimization_algorithm import OptimizationAlgorithm
from scipy.optimize import differential_evolution


class DifferentialEvolution(OptimizationAlgorithm):
    def __init__(self):
        super().__init__(name="Differential Evolution")

    def optimize(self, fitness_func, bounds):

        result = differential_evolution(fitness_func, bounds)

        return result
