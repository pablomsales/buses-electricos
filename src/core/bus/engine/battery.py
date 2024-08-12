class Battery:

    def __init__(self, capacity, num_cycles, state, voltage):
        self._capacity = (capacity,)
        self._num_cycles = num_cycles
        self.state = state
        self._voltage = voltage
