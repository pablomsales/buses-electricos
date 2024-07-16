class Bus:

    def __init__(self, mass):
        self._mass = 0

    @property
    def mass(self):
        return self._mass

    @mass.setter
    def mass(self, valor):
        if valor > 0:
            self._mass += valor
