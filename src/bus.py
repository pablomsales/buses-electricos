class Bus:

    def __init__(self, mass):
        self._mass = 0

    @property
    def mass(self):
        return self._mass

    @mass.setter
    def mass(self, value):
        if value > 0:
            self._mass += value
