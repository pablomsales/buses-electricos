class OptimizationAlgorithm:

    def __init__(self, name):
        self.name = name

    def optimize(self, fitness_func, parameters):
        raise NotImplementedError("This method should be implemented by subclasses")
