class Parameter:

    def __init__(self, min_value, max_value, units):
        self.min_value = min_value
        self.max_value = max_value
        self.units = units
        self.range = (min_value, max_value)
